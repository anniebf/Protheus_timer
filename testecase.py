from tir import Webapp , PouiInternal
import graph
import time
# Inside __init__ method in Webapp class of main.py
def __init__(self, config_path="", autostart=True):
    self.__webapp = PouiInternal(config_path, autostart)
import unittest

menulateral = 'Compras > Movimento > Pedidos de Compra'

class teste1(unittest.TestCase):

    @classmethod
    def setUpClass(inst):
        print("Configurando o ambiente de teste...")
        inst.oHelper = Webapp()
        driver = inst
        def mock_log_info(*args, **kwargs):
            print("Ignorando navegação automática do menu 'Sobre'...")
            return True
        
        # Aplicando o patch no objeto interno (WebappInternal)
        inst.oHelper._Webapp__webapp.GetLogInfo = mock_log_info
        # ---------------------------------------

        # Agora o Setup deve apenas logar e parar
        inst.oHelper.Setup('SIGAADV', '', '16', '', '09')

        #inst.oHelper.SetLateralMenu(f"{menulateral}")

        script_protheus = """
            function setProtheusValue(selector, value) {
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

                let host = findInShadows(selector);
                if (host && host.shadowRoot) {
                    let input = host.shadowRoot.querySelector('input');
                    if (input) {
                        input.value = value;
                        // Dispara eventos para o Protheus entender que houve digitação
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                        return true;
                    }
                }
                return false;
            }
            return setProtheusValue('wa-text-input#COMP4506', arguments[0]);
        """
        for i in range(5):
            sucesso = driver.execute_script(script_protheus, codigoMfa)
            if sucesso:
                print("Token inserido com sucesso!")
                # Agora clica no botão OK (COMP4507)
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
                break
            else:
                print(f"Tentativa {i+1}: Aguardando tela de MFA...")
                time.sleep(2)

        script_fechar = """
            function clickProtheusElement(selector) {
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

                let host = findInShadows(selector);
                // Verifica se o host existe e se possui o shadowRoot aberto
                if (host && host.shadowRoot) {
                    // No caso do wa-button, o botão real está dentro do shadowRoot
                    let innerBtn = host.shadowRoot.querySelector('button');
                    if (innerBtn) {
                        innerBtn.click();
                        return true;
                    }
                }
                return false;
            }
            return clickProtheusElement('wa-button#COMP4513');
        """

        # Execução
        sucesso_fechar = driver.execute_script(script_fechar)
        if sucesso_fechar:
            print("Botão Fechar clicado!")
        else:
            print("Não foi possível encontrar o botão COMP4513.")

    '''def test_00(self):
        self.oHelper.SetValue('Programa Inicial','SIGAADV')
        self.oHelper.SetValue('Ambiente no servidor','debug')'''

    def test_01(self):
        print("Acessando menu lateral")
        self.oHelper.SetLateralMenu(f"{menulateral}")
        print("Executando teste 01")
        self.oHelper.SetButton("Visualizar")
        self.oHelper.SetButton("Cancelar")
        self.oHelper.SetButton('x')

    @classmethod
    def tearDownClass(inst):
	    inst.oHelper.TearDown()
            
if __name__ == '__main__':
	unittest.main()