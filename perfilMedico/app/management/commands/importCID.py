from django.core.management.base import BaseCommand
import pandas as pd
from app.models import CID

class Command(BaseCommand):
    help = 'Import data from CSV to Django models'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        df = pd.read_csv(csv_file, sep=";", encoding='latin-1')

        df = df[['DESCRICAO','DESCRABREV']]
        
        lista = []

        for index, row in df.iterrows():
            codigo = str(row['DESCRABREV']).split()[0]
            lista.append(codigo)

        df["codigo"] = lista
        df = df[['DESCRICAO','codigo']]

        for index, row in df.iterrows():
            self.stdout.write(self.style.NOTICE("Adicionando: " + row['codigo'] + " - " + row["DESCRICAO"]))
            CID.objects.create(
                codigo = row['codigo'],
                descricao = row["DESCRICAO"]
            )
            self.stdout.write(self.style.SUCCESS("Dados importados com sucesso"))
        

        self.stdout.write(self.style.SUCCESS("Finalização do processo!"))
