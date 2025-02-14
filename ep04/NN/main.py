'''
    Script principal, que chama as funcoes dos outros modulos para
    carregar os dados, fazer o pre-processmanto e adequacao, instanciar
    uma rede neural e treina-la, utilizando os dados processados.
'''

from data import load_data, process_data, min_max
from model import NN2
from train import split_data, train_network
import torch, time

LEARNING_RATE = 0.001
MODEL_PATH = ['./trained_nn/igG.pt', 
              './trained_nn/igM.pt',
              './trained_nn/PCR.pt']

if __name__ == "__main__":
    
    print('\nCARREGANDO DADOS...')
    data = load_data()
    start = time.time()
    min_max(data)
    for exam_type, name in [(0,'IGG'), (1,'IGM'), (2,'PCR')]:

        print('\n------------------------\n')
        print('[REDE ' + name + '] SEPARANDO DADOS PARA TREINAMENTO...')
        processed_data = process_data(data, exam_type)

        print('[REDE ' + name + '] ADEQUANDO DADOS PARA TREINAMENTO...')
        splitted_data = split_data(processed_data)

        print('[REDE ' + name + '] MONTANDO MODELO...')
        x_train = splitted_data[0]
        y_train = splitted_data[2]

        print('[REDE ' + name + '] ' + str(len(x_train)) + \
                ' ELEMENTOS NO CONJUNTO DE TREINAMENTO...')
        print('[REDE ' + name + '] ' + str(len(y_train)) + \
                ' ELEMENTOS NO CONJUNTO DE VALIDAÇÃO...')

        print('[REDE ' + name + '] INSTANCIANDO REDES...')
        network = NN2(x_train.shape[1])
        optimizer = torch.optim.Adam(network.parameters(), lr=LEARNING_RATE)
        criterion = torch.nn.BCELoss()

        print('[REDE ' + name + '] TREINANDO...\n')
        train_network(splitted_data, network, optimizer, criterion, \
                      MODEL_PATH[exam_type], True, True)

        print('MODELO TREINADO. (Salvo em ' + MODEL_PATH[exam_type] + ')')

    end = time.time()
    print('\nTEMPO GASTO: %.2fs'%(end-start))
    print('FIM.')
