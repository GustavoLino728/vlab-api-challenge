import asyncio
import os
import random
from decimal import Decimal

import httpx
from faker import Faker

API_URL = "http://api:8000/api/v1/abastecimentos"
NUM_REQUESTS = 100
INTERVAL_SECONDS = 1

API_KEY = os.getenv("API_KEY", "changeme")  # mesmo nome que o Settings usa

fake = Faker("pt_BR")


def generate_valid_cpf() -> str:
    return fake.cpf()


def generate_abastecimento() -> dict:
    tipos = ["GASOLINA", "ETANOL", "DIESEL"]
    return {
        "id_posto": random.randint(1, 10),
        "data_hora": fake.date_time_this_year().isoformat(),
        "tipo_combustivel": random.choice(tipos),
        "preco_por_litro": float(round(Decimal(random.uniform(3.0, 7.0)), 3)),
        "volume_abastecido": float(round(Decimal(random.uniform(1.0, 100.0)), 3)),
        "cpf_motorista": generate_valid_cpf(),
    }


async def send_request(session: httpx.AsyncClient, data: dict):
    headers = {"X-API-Key": API_KEY}
    try:
        response = await session.post(API_URL, json=data, headers=headers)
        if response.status_code == 201:
            print(f"Enviado: {data['cpf_motorista']} - {response.status_code}")
        else:
            print(f"Erro {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Erro na requisição: {e}")


async def main():
    async with httpx.AsyncClient(timeout=30) as session:
        tasks = []
        for _ in range(NUM_REQUESTS):
            data = generate_abastecimento()
            tasks.append(send_request(session, data))
            await asyncio.sleep(INTERVAL_SECONDS)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
