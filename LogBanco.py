from datetime import datetime
import oracledb
import MandaEmail
import json
from dotenv import load_dotenv
import glob
import os
from time import sleep

def get_latest_log_file(log_folder='log', log_prefix='log'):
    log_files = glob.glob(os.path.join(log_folder, f'{log_prefix}*.txt'))
    if not log_files:
        log_files = glob.glob(f'{log_prefix}*.txt')
    log_files.sort(key=os.path.getmtime, reverse=True)
    return log_files[0] if log_files else None

load_dotenv()
username = os.getenv('username')
password = os.getenv('password')
dsn = os.getenv('dsn')
usuario = os.getenv('usuario')

# Carregar dados de configuração
with open('config.json', 'r') as file:
    dados = json.load(file)
sistema = 'PROTHEUS'

erro_tratado_erro = False
erro_tratado_war = False
tempo_executado = 0  # Inicializa a variável

def is_valid_timestamp(timestamp_str):
    try:
        datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def resultado():
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT TEMPO_EXECUCAO FROM RPA.TIMER 
        WHERE DESCRICAO = 'FINALIZANDO PROTHEUS_TIR' 
        FETCH FIRST ROW ONLY
    """)
    ultimo_resultados = cursor.fetchone()
    ultimo_resultado = ultimo_resultados[0] if ultimo_resultados else 0
    connection.close()
    return ultimo_resultado

def registrar_timer(descricao, sistema, usuario, erro, tempo_execucao, timestamp_str):
    if not is_valid_timestamp(timestamp_str):
        timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO RPA.TIMER (DESCRICAO, SISTEMA, USUARIO, ERRO, TEMPO_EXECUCAO, HORARIO_EXECUCAO)
            VALUES (:descricao, :sistema, :usuario, :erro, :tempo_execucao, TO_TIMESTAMP(:timestamp_str, 'YYYY-MM-DD HH24:MI:SS'))
        """, {
            'descricao': descricao,
            'sistema': sistema,
            'usuario': usuario,
            'erro': erro,
            'tempo_execucao': tempo_execucao,
            'timestamp_str': timestamp_str
        })
        connection.commit()
    except Exception as e:
        print(f"Erro ao inserir no banco: {e}")
    finally:
        connection.close()

def inicio():
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    registrar_timer('INICIANDO PROTHEUS_TIR', sistema, usuario, 'OK', 0, data_atual)
    print('Início registrado no banco')

def salvar():
    global erro_tratado_erro, erro_tratado_war, tempo_executado
    
    sleep(10)
    arquivo_log = get_latest_log_file()
    if not arquivo_log:
        print("Nenhum arquivo de log encontrado!")
        return
    
    print(f"Processando arquivo: {arquivo_log}")
    
    last_timestamp = None
    with open('./log/log.txt', "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()  # Remove espaços e quebras de linha
            
            # Processa linhas especiais (Ran/OK) mesmo sem timestamp
            if linha.startswith("Ran") and " in " in linha:
                try:
                    tempo_str = linha.split(" in ")[1].replace("s", "").split(".")[0]
                    tempo_executado = int(tempo_str)
                    print(f"Tempo de execução capturado: {tempo_executado}s")
                    continue
                except (ValueError, IndexError) as e:
                    print(f"Erro ao capturar tempo: {e}")
                    continue
            
            if linha.lower() == "ok":
                if tempo_executado:
                    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    registrar_timer(
                        'FINALIZANDO PROTHEUS_TIR', 
                        sistema, 
                        usuario, 
                        'OK', 
                        tempo_executado,
                        data_atual
                    )
                    print("Registro final OK gravado no banco")
                continue
            if "FAILED" in linha:
                MandaEmail.enviar_warning('falha no processo')
            
            # Processa apenas linhas com timestamp
            if len(linha) < 19:
                continue
                
            timestamp_str = linha[:19]
            
            if is_valid_timestamp(timestamp_str):
                new_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                tempo_execucao = 1  # Valor padrão
                
                if last_timestamp:
                    delta = new_timestamp - last_timestamp
                    tempo_execucao = delta.total_seconds()
                
                last_timestamp = new_timestamp
            else:
                timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                tempo_execucao = 1
            
            try:
                if "INFO" in linha:
                    descricao = linha[29:-1].strip().replace("'", "''")
                    registrar_timer(descricao, sistema, usuario, 'OK', tempo_execucao, timestamp_str)
                
                elif "WARNING:" in linha and not erro_tratado_war:
                    descricao = linha[34:].strip().replace("'", "''")
                    registrar_timer(descricao, sistema, usuario, 'WARN', tempo_execucao, timestamp_str)
                    erro_tratado_war = True
                    
            except Exception as e:
                print(f"Erro ao processar linha: {linha}\nErro: {e}")
    
    # Verificação final
    ultimo_resultado = resultado()
    if ultimo_resultado and tempo_executado and ultimo_resultado >= tempo_executado * 1.3:
        MandaEmail.enviar_temp_exc()
    else:
        print('Tempo de execução dentro do esperado')

if __name__ == '__main__':
    inicio()
    salvar()