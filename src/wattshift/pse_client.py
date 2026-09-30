import asyncio
from datetime import datetime, timezone
import httpx
from pydantic import BaseModel, Field


class EnergyPriceEntry(BaseModel):
    udt_time: str = Field(alias="udtczas")
    price_pln_mwh: float = Field(alias="rce_pln")


async def fetch_pse_rce() -> list[dict]:
    # Endpoint PSE publikujący rynkowe ceny energii
    url = "https://api.raporty.pse.pl/api/rce-pln?$top=24"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def main():
    print("Pobieranie ostatnich stawek cenowych z PSE...")
    try:
        raw_data = await fetch_pse_rce()
        # Wyświetlamy 3 pierwsze wpisy dla weryfikacji
        for item in raw_data[:3]:
            entry = EnergyPriceEntry.model_validate(item)
            print(f"Godzina: {entry.udt_time} -> Cena: {entry.price_pln_mwh:.2f} PLN/MWh")
        print(f"\nŁącznie pobrano wpisów: {len(raw_data)}. Połączenie z PSE działa prawidłowo!")
    except Exception as e:
        print(f"Błąd podczas komunikacji z PSE: {e}")


if __name__ == "__main__":
    asyncio.run(main())