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

        inst.oHelper.Setup('SIGAADV', '', '16', '', '09')

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