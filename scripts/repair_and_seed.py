import asyncio
import os
import sys
from sqlalchemy import select

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import async_session
from core.models import Product, Category

async def repair():
    async with async_session() as session:
        # Словник: Німецька (те, що зараз у полі 'name') -> Українська
        corrections = {
            "Nacken ohne Knochen": "Ошийок без кістки",
            "Hackfleisch vom Schwein": "Фарш свинячий",
            "Schnitzel / Braten": "Шніцель / Печеня",
            "Lummersteaks": "Люммерстейк",
            "Filet (Schwein)": "Філе (Свинина)",
            "Dicke Rippe": "Товсте ребро",
            "Spareribs": "Реберця (Spareribs)",
            "Bauchfleisch": "Грудинка",
            "Schinkenbraten": "Шинка для запікання",
            "Kotelett": "Котлета (Kotelett)",
            "Gehacktes halb & halb": "Фарш асорті",
            "Rindfleisch ohne Knochen": "Яловичина без кістки",
            "Rinderhackfleisch": "Яловичий фарш",
            "Rouladen / Braten": "Рулади (Яловичина)",
            "Suppenfleisch": "Супове м'ясо",
            "Beinscheibe": "Голяшка (Beinscheibe)",
            "Entrecote / Rumpsteak": "Антрекот",
            "Filet (Rind)": "Філе (Яловичина)",
            "Bratwurst": "Братвурст",
            "Fleischwurst": "Варена ковбаса",
            "Mettwurst": "Меттвурст",
            "Leberwurst": "Печінкова ковбаса",
            "Grützwurst": "Грютцвурст"
        }

        # 1. Продукти: переносимо німецьку в name_de, записуємо українську в name
        for de, uk in corrections.items():
            res = await session.execute(select(Product).where(Product.name == de))
            p = res.scalar_one_or_none()
            if p:
                p.name = uk
                p.name_de = de

        # 2. Категорії: виправляємо за слагом
        cat_map = {
            "schwein": {"uk": "Свинина", "de": "Schwein"},
            "rind": {"uk": "Яловичина", "de": "Rind"},
            "wurst": {"uk": "Ковбаси", "de": "Wurst"},
            "mix": {"uk": "Мікс", "de": "Mix"}
        }
        for slug, names in cat_map.items():
            res = await session.execute(select(Category).where(Category.slug == slug))
            c = res.scalar_one_or_none()
            if c:
                c.name = names["uk"]
                c.name_de = names["de"]

        await session.commit()
        print("✅ Дані виправлено успішно.")

if __name__ == "__main__":
    asyncio.run(repair())