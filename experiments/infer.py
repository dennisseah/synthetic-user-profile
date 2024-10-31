import asyncio
import json
import os

import pandas as pd

from experiments.models import ProfileChoice, Result
from synthetic_user_profile.hosting import container
from synthetic_user_profile.protocols.i_azure_openai_service import IAzureOpenAIService

openai_service = container[IAzureOpenAIService]


async def to_buy(profile: ProfileChoice, product: str) -> Result:
    yeses = 0
    tries = 8
    for _ in range(tries):
        decision = await openai_service.generate(
            [
                {
                    "role": "system",
                    "content": "You are a decision maker and your profile is "
                    "below (bounded by triple quotes). Please make a decision on "
                    f"buying a {product} for Christmas.\n "
                    "Please provide reasonings for your answer. And in a separate "
                    "line provide with '[Yes]' for yes and '[No]' for no."
                    + f'''
                        """
                        {profile.generated}
                        """
                        ''',
                }
            ],
            temperature=0.5,
        )
        if (
            decision.choices[0].message.content
            and decision.choices[0].message.content.find("[Yes]") != -1
        ):
            yeses += 1

    return Result(**profile.model_dump(), decision=(yeses / tries))


async def main(product: str):
    inputs = json.load(open(os.path.join("experiments", "profiles.json"), "r"))
    profiles: list[ProfileChoice] = [ProfileChoice(**p) for p in inputs["profiles"]]

    all_results = await asyncio.gather(*[to_buy(p, product) for p in profiles])

    data: list[dict[str, str | float]] = [r.model_dump() for r in all_results]
    df = pd.DataFrame(data)
    df.drop("generated", axis=1, inplace=True)
    df.sort_values(
        ["state", "annual_income_k", "gender"], inplace=True, ignore_index=True
    )
    print(df)


if __name__ == "__main__":
    asyncio.run(main("Peloton Indoor Exercise Bike"))
