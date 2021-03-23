import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from utils import format_percent, format_money

class Spreadsheet:
    def __init__(self):
        """
        Inicializa as variáveis do construtor.
        Necessário definir o scope dos serviços a acessar.
        Indicar o diretório do arquivo json com as credenciais 
        para acessar a api.
        Informar o código chave da planilha a ser visualizada.

        Requer
            - scopes : Type [list]
            - credential : Type [str]
            - key_plan : Type [str]
        """

        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        self.credential = 'credentials.json'
        self.key_plan = '1zvqjX-0tB0lkZ0cLphtP2Z5N-EtRzfBCZawSpoP9JFc'
        self.gc = self.auth()


    def auth(self):
        """
        Função para fazer a autenticação no serviço Google.

        Retorna
            - gspread auth
        """

        credentials = Credentials.from_service_account_file(self.credential)
        scoped_credentials = credentials.with_scopes(self.scopes)
        return gspread.authorize(scoped_credentials)

    def read_sheet(self):
        """
        Função para carregar os dados da planilha informada.
        Os dados são populados em um dataframe da lib pandas.

        Retorna
            - pandas dataframe
        """

        sheet = self.gc.open_by_key(self.key_plan)
        tab = sheet.worksheet('Dados')
        registers = tab.get_all_records()
        return pd.DataFrame(registers)

    def export_empty(self, dataframe):
        """
        Função para gerar arquivo csv com os dados ausentes
        de cada coluna do dataframe.

        Args:
            - dataframe : Type [pandas dataframe]

        Gera
            - arquivo csv da coluna data
            - arquivo csv da coluna item
            - arquivo csv da coluna valor
            - arquivo csv da coluna imposto
        """

        for col in dataframe.columns:
            new_df = dataframe[(dataframe[col] == "")]
            new_df.index.name = 'Index'
            new_df.to_csv(f'{col.lower()}_vazio.csv')

    def sanitize_dataframe(self, dataframe):
        """
        Função que faz o tratamento dos valores para
        padronização.
        Os registros que estão vazios são removidos do
        dataframe ainda que apenas um campo esteja ausente.
        É aplicado uma função para correção dos valores
        percentuais.
        É aplicado uma função para correção dos valores
        monetários.

        Args:
            - dataframe : Type [pandas dataframe]

        Retorna
            - pandas dataframe
        """

        dataframe.replace("", float("NaN"), inplace=True)
        df = dataframe.dropna()
        df.loc[:, 'Imposto'] = df['Imposto'].apply(format_percent)
        df.loc[:, 'Valor'] = df.Valor.apply(format_money)
        return df

    def export_csv(self, dataframe):
        """
        Função que faz a geração de um arquivo csv
        após todos os tratamentos e conversões no 
        dataframe com os valores coletados da planilha.

        Args:
            - dataframe : Type [pandas dataframe]

        Gera
            - arquivo csv
        """

        dataframe.to_csv('planilha_tratada_convertida.csv', index=False)

if __name__ ==  "__main__":
    client = Spreadsheet()
    dataframe = client.read_sheet()
    client.export_empty(dataframe)
    df = client.sanitize_dataframe(dataframe)
    client.export_csv(df)
