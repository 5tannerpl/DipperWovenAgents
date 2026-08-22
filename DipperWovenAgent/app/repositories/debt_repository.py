from app.common.database import get_db_pool


class DebtRepository:

    async def get_random_debt_id(self) -> int | None:
        pool = get_db_pool()

        row = await pool.fetchrow(
            """
            SELECT debt_id
            FROM debt_id_reg
            ORDER BY RANDOM()
            LIMIT 1
            """
        )

        if row is None:
            return None

        return row["debt_id"]


debt_repository = DebtRepository()