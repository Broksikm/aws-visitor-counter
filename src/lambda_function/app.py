import boto3
import os
import json
import logging

# Nastavení loggeru pro lepší ladění
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicializace klienta pro DynamoDB mimo handler pro znovupoužití
dynamodb = boto3.resource('dynamodb')

# Získání názvu tabulky z environment variable, kterou nastaví CloudFormation
TABLE_NAME = os.environ.get('TABLE_NAME')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Tato funkce se spustí pokaždé, když API Gateway přijme požadavek.
    """
    logger.info(f"Request received for table: {TABLE_NAME}")

    try:
        # Atomic update: Zvýší atribut 'visits' o 1. Pokud neexistuje, vytvoří ho s hodnotou 1.
        # Je to bezpečnější než čtení a následný zápis.
        response = table.update_item(
            Key={'id': 'visitor_count'},
            UpdateExpression='SET visits = if_not_exists(visits, :start) + :inc',
            ExpressionAttributeValues={
                ':inc': 1,
                ':start': 0
            },
            ReturnValues='UPDATED_NEW'
        )
        
        # Získání nové hodnoty počítadla z odpovědi
        new_count = response['Attributes']['visits']
        logger.info(f"Successfully updated counter. New count is: {new_count}")

        # Úspěšná odpověď pro API Gateway
        return {
            'statusCode': 200,
            'headers': {
                # Tyto hlavičky jsou důležité pro CORS
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'count': int(new_count)})
        }

    except Exception as e:
        logger.error(f"Error updating counter: {e}")
        # Chybová odpověď pro API Gateway
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'error': 'Could not update the counter.'})
        }