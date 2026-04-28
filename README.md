# Protheus Timer

## Descrição

O **Protheus Timer** é um projeto de automação desenvolvido para monitorar e registrar o tempo de execução de testes automatizados no sistema Protheus, utilizando a biblioteca TIR (Totvs Interface Robot). O projeto executa scripts de teste a cada 1 hora, registra logs no banco de dados Oracle e envia notificações por email em caso de erros, warnings ou tempos de execução elevados.

## Funcionalidades

- **Execução de Testes Automatizados**: Utiliza Selenium e TIR para executar testes no Protheus.
- **Registro de Tempos**: Registra o tempo de execução de cada etapa no banco de dados Oracle.
- **Monitoramento de Logs**: Processa arquivos de log para identificar erros e warnings.
- **Notificações por Email**: Envia alertas automáticos para destinatários configurados em caso de problemas.
- **Comparação de Performance**: Verifica se o tempo de execução atual excede 30% do tempo da última execução bem-sucedida.

## Pré-requisitos

- Python 3.8 ou superior
- Banco de dados Oracle com tabela `RPA.TIMER`
- Conta de email SMTP para notificações
- Navegador Firefox (configurado no `config.json`)
- Variáveis de ambiente configuradas em um arquivo `.env`:
  - `usernamedb`: Usuário do banco de dados
  - `password`: Senha do banco de dados
  - `dsn`: DSN do Oracle
  - `usuario`: Usuário do sistema
  - `server_smtp`: Servidor SMTP
  - `port`: Porta SMTP
  - `sender_mail`: Email do remetente
  - `password`: Senha do email

## Instalação

1. Clone ou baixe o repositório para o diretório desejado.
2. Instale as dependências Python:
   ```
   pip install -r requirements.txt
   ```
3. Configure o arquivo `config.json` com as informações do ambiente Protheus.
4. Crie um arquivo `.env` na raiz do projeto com as variáveis de ambiente necessárias.
5. Certifique-se de que o banco de dados Oracle esteja acessível e a tabela `RPA.TIMER` exista com a estrutura adequada.

## Uso

### Execução Principal

Execute o script principal para iniciar os testes:

```bash
python executar_main.py
```

Ou utilize o script PowerShell:

```powershell
.\executar_protheus_timer.ps1
```

### Scripts Individuais

- **main.py**: Executa o script Selenium para automação no Protheus.
- **mainTir.py**: Executa os testes unitários usando unittest e registra logs.
- **LogBanco.py**: Processa logs e registra informações no banco de dados.
- **MandaEmail.py**: Módulo para envio de emails de notificação.

### Estrutura de Logs

Os logs são salvos na pasta `log/` com o nome `log.txt`. O sistema processa o arquivo para extrair tempos de execução e identificar problemas.

## Estrutura do Projeto

```
Protheus_timer/
├── config.json              # Configurações do ambiente Protheus
├── executar_main.py         # Script principal de execução
├── executar_protheus_timer.ps1  # Script PowerShell para execução
├── graph.py                 # (Arquivo adicional, possivelmente para gráficos)
├── LogBanco.py              # Módulo para interação com banco de dados
├── main.py                  # Script de automação Selenium
├── mainTir.py               # Execução de testes TIR
├── MandaEmail.py            # Módulo de envio de emails
├── requirements.txt         # Dependências Python
├── testecase.py             # Casos de teste unitários
└── log/
    └── log.txt              # Arquivo de log
```


## Suporte

Em caso de dúvidas ou problemas, entre em contato com a equipe de RPA da Bom Futuro.