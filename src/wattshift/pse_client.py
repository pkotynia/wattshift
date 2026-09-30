import asyncio
from datetime import datetime
import httpx
from pydantic import BaseModel, Field


class EnergyPriceEntry(BaseModel):
    timestamp_str: str = Field(alias="dtime")
    period_range: str = Field(alias="period")  # format np. "00:00 - 00:15"
    price_pln_mwh: float = Field(alias="rce_pln")

    @property
    def price_pln_kwh(self) -> float:
        """Przeliczenie stawki z MWh na kWh (bardziej czytelne dla domu)"""
        return self.price_pln_mwh / 1000.0


async def fetch_pse_rce(target_date: str | None = None) -> list[dict]:
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

    url = "https://api.raporty.pse.pl/api/rce-pln"
    # Doba ma 96 kwadransów po 15 min
    params = {
        "$filter": f"business_date eq '{target_date}'",
        "$first": 96,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict) and "value" in data:
            return data["value"]
        if isinstance(data, list):
            return data
        return []


async def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Pobieranie 15-minutowych stawek z PSE dla daty {today}...")
    try:
        records = await fetch_pse_rce(today)
        if not records:
            print("Brak opublikowanych danych dla podanej daty.")
            return

        print(f"Łącznie pobrano punktów pomiarowych: {len(records)}\n")
        # Wyświetlamy pierwsze 8 kwadransów (pierwsze 2 godziny doby)
        for item in records[:8]:
            entry = EnergyPriceEntry.model_validate(item)
            print(
                f"Przedział: {entry.period_range:<13} | "
                f"Cena MWh: {entry.price_pln_mwh:>8.2f} zł | "
                f"Cena kWh: {entry.price_pln_kwh:>6.3f} zł"
            )

        print("\nSukces! Model Pydantic zmapował dane bezbłędnie.")
    except httpx.HTTPStatusError as e:
        print(f"Błąd HTTP: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")


if __name__ == "__main__":
    asyncio.run(main())