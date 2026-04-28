import unittest
from testecase import teste1
import time
import LogBanco
import sys
from time import sleep

def exec_tir():
    try:
        # Abre o arquivo de log
        log_file = open('Log\log.txt', 'w')
        
        # Redireciona a saída padrão e de erro
        sys.stdout = sys.stderr = log_file

        print('------------------------')
        print('comecando o programa')
        print('------------------------')

        time.sleep(1)
        suite = unittest.TestSuite()
        print('entrando nos testes individuais')

        suite.addTest(teste1('test_01'))

        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)  # Armazena o resultado para verificação
        
        print('------------------------')
        print('finalizando o programa')
        print('------------------------')

    except Exception as e:
        print(f'ocorreu algum erro na execução do tir: {str(e)}')
    finally:
        # Restaura os fluxos padrão primeiro
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        
        # Fecha o arquivo de log para garantir que tudo foi escrito
        log_file.close()
        
        # Aguarda um pouco para garantir que o sistema de arquivos tenha terminado as operações
        sleep(5)
        
        # Agora chama a função salvar
        LogBanco.salvar()

if __name__ == "__main__":
    exec_tir()