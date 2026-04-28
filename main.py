from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import os
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import time

import graph

with open('./config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(data['Url'])
url = data['Url']
username = data['User']
passsword = data['Password']

load_dotenv()
Rotina = os.getenv('Setup_rotina')
Ambiente = os.getenv('Setup_ambiente')
Emp = os.getenv('Setup_emp')
Filial = os.getenv('Setup_filial')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--mute-audio')
options.add_argument("--disable-gpu")
options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=options)
driver.get(url)

def exec_selenium_script():
        
    rotina = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//wa-combobox[@id="selectStartProg"]')))
    rotina.send_keys(Rotina)

    ambiente = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, '//wa-combobox[@id="selectEnv"]')))
    ambiente.send_keys(Ambiente)


    botao = WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("""
            const dialog = document.querySelector('body > wa-dialog.startParameters.style-plastique');
            if (!dialog || !dialog.shadowRoot) return null;
            const waButton = dialog.shadowRoot.querySelector('footer > wa-button:nth-child(2)');
            if (!waButton || !waButton.shadowRoot) return null;
            const button = waButton.shadowRoot.querySelector('button');
            return button;  """))

    print('acessou o sigaadv')
    driver.execute_script("arguments[0].click();", botao)
    sleep(10)

    print('clicando botao ok')

    try:
        
        tela_tamanho = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'wa-button#COMP3012'))
        )
        if tela_tamanho:
        
            print("Tela de tamanho carregada, clicando no botão...")
            shadow_webview = tela_tamanho.shadow_root
            botao = shadow_webview.find_element(By.CSS_SELECTOR, "button")
            driver.execute_script("arguments[0].click();", botao)
            print("Botão de tamanho clicado com sucesso!")
            
    except:
        
        print('nao apareceu a tela de redimensao de tamanho do navegador')


    """Realiza login dentro do iframe do wa-webview."""

    wa_webview = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'wa-webview#COMP3010')))
    shadow_webview = wa_webview.shadow_root
    iframe = shadow_webview.find_element(By.CSS_SELECTOR, "iframe")
    driver.switch_to.frame(iframe)
    sleep(5) 

    login = driver.find_elements(By.NAME, 'login')[1]
    login.clear()
    login.send_keys(username)

    driver.find_elements(By.NAME, 'password')[1].send_keys(passsword)

    driver.find_element(By.XPATH,'/html/body/ld-root/ng-component/pro-login/po-page-login/po-page-background/div/div/div[2]/div/form/div/po-button/button').click()
    sleep(5)

    entrar = driver.find_elements(By.XPATH, '/html/body/ld-root/ng-component/pro-session-settings/pro-page-background/div/div/div[1]/div/form/div/div[2]/po-button[2]/button')
    for btn in entrar:
        if 'Entrar' in btn.text:
            btn.click()
            
            break
    sleep(10)


    get_iframe_script = """let webview = document.querySelector('wa-webview#COMP3010');
        if (webview && webview.shadowRoot) {
            return webview.shadowRoot.querySelector('iframe');
        }
        return null;
        """

    try:

        wait = WebDriverWait(driver, 20)
        
        # Substitua 'iframe_seletor' pelo seletor real do seu iframe (ex: "iframe[src*='protheus']")
        iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
        print("Entrou no iframe com sucesso!")

        # 2. Agora que estamos dentro do iframe, buscamos o Host do Shadow DOM
        shadow_host = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'wa-webview#COMP3010')))
        print("Host do Shadow DOM (wa-webview) encontrado!")

        # 3. Acessar o Shadow Root
        shadow_root = shadow_host.shadow_root

        # 4. Buscar o input de data dentro do Shadow Root
        # O Selenium às vezes precisa de um pequeno delay para o shadow carregar o conteúdo interno
        time.sleep(2) 
        
        input_base_date = shadow_root.find_element(By.CSS_SELECTOR, 'input[name="base_date"]')
        
        # Limpar e preencher
        input_base_date.clear()
        input_base_date.send_keys("20/04/2026")
        print("Data preenchida com sucesso!")

        # Tenta localizar o iframe via JS (com retry manual se necessário)
        iframe_element = None
        for _ in range(10):  # tenta por 10 segundos
            iframe_element = driver.execute_script(get_iframe_script)
            if iframe_element:
                break
            sleep(1)

        if iframe_element:
            # 2. Entra no iframe
            driver.switch_to.frame(iframe_element)
            print("Entramos no iframe do Shadow DOM!")

            # 3. Agora busca os campos de Grupo e Filial (usando seletores mais flexíveis)
            wait = WebDriverWait(driver, 20)
            
            # Como o ID parece ser dinâmico (GUID), vamos usar o atributo 'data-placeholder' 
            # ou parte do ID se possível. Vou manter seu XPATH, mas recomendo 'contains'.
            
            grupo = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@id, 'po-lookup')]")))
            grupo.clear()
            grupo.send_keys(Emp)
            
            # Para a filial, se houver dois campos parecidos, pegamos o segundo ou pelo ID completo
            botao_entrar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Entrar']]")
            ))

            # 2. Clica no botão
            botao_entrar.click()
    except Exception as e:
        print('nao apareceu a tela de grupo')
        #print(f"Erro: {e}")
        entrar = driver.find_elements(By.XPATH, '/html/body/ld-root/ng-component/pro-session-settings/pro-page-background/div/div/div[1]/div/form/div/div[3]/po-button[2]/button')
        for btn in entrar:
            if 'Entrar' in btn.text:
                btn.click()
                break    
        
    sleep(15)


    driver.switch_to.default_content()

    script_localizador = """
        function findInShadows(sel, root = document) {
            let el = root.querySelector(sel);
            if (el) return el;
            let hosts = root.querySelectorAll('*');
            for (let h of hosts) {
                if (h.shadowRoot) {
                    let f = findInShadows(sel, h.shadowRoot);
                    if (f) return f;
                }
            }
            return null;
        }
        
        // Encontra o componente pai (host)
        let host = findInShadows('wa-text-input#COMP4506');
        if (host && host.shadowRoot) {
            // Retorna o input real que está dentro do Shadow DOM
            return host.shadowRoot.querySelector('input');
        }
        return null;
    """

    input_mfa = driver.execute_script(script_localizador)

    try:
        
        
        if input_mfa:
            #
            #GRAPH - OBTENDO CÓDIGO MFA 
            #
            graph_client = graph.MicrosoftGraphClient()
            codigoMfa = graph_client.obter_ultimo_codigo_acesso()
            codigoMfa = codigoMfa.strip()  
            codigoMfa = int(codigoMfa)  
            print("Código MFA obtido:", codigoMfa)
            print(type(codigoMfa))
            
            
            input_mfa.clear()
            input_mfa.click() 
            
            # Digita o código
            input_mfa.send_keys(codigoMfa)
            
            print("Código inserido com sucesso via Selenium.")
            driver.execute_script("""
                function findBtn(sel, root = document) {
                    let el = root.querySelector(sel);
                    if (el) return el;
                    let hosts = root.querySelectorAll('*');
                    for (let h of hosts) {
                        if (h.shadowRoot) {
                            let f = findBtn(sel, h.shadowRoot);
                            if (f) return f;
                        }
                    }
                    return null;
                }
                let btn = findBtn('wa-button#COMP4507');
                if (btn && btn.shadowRoot) btn.shadowRoot.querySelector('button').click();
            """)
    except Exception as e:
        print(f"Nao foi localizado a tela mfa ou ocorreu um erro: {e}")
        
    driver.close()
    
if __name__ == "__main__":
    exec_selenium_script()
