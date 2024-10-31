import asyncio
import json
import os

from experiments.models import ProfileChoice
from synthetic_user_profile.hosting import container
from synthetic_user_profile.protocols.i_azure_openai_service import IAzureOpenAIService

openai_service = container[IAzureOpenAIService]


states = ["Washington", "Oregan", "California"]
annual_incomes = [70, 100, 150]

profile_choices = [ProfileChoice(gender="male", state=state) for state in states] + [
    ProfileChoice(gender="female", state=state) for state in states
]


async def generate(profile_choice: ProfileChoice) -> ProfileChoice:
    result = await openai_service.generate(
        [
            {
                "role": "system",
                "content": "You are a prompt engineer. You are asked to create "
                f"a fictional {profile_choice.gender} consumer of a particular brand. "
                f"This person lives in the {profile_choice.state} State of the US, "
                "The person is married and has an annual household income of "
                f"{profile_choice.annual_income_k} thousand dollars. Please include "
                "the person name, age, demographic, personality traits, and interests.",
            }
        ],
        temperature=0,
        seed=1000,
    )

    if not result.choices[0].message.content:
        raise Exception("Failed to generate response")
    profile_choice.generated = result.choices[0].message.content
    return profile_choice


async def main():
    def create_profile_choice(profile_choice: ProfileChoice, income: int):
        params = profile_choice.model_dump()
        params["annual_income_k"] = income
        return ProfileChoice(**params)

    profiles = []
    for income in annual_incomes:
        all_groups = await asyncio.gather(
            *[generate(create_profile_choice(p, income)) for p in profile_choices]
        )
        profiles += all_groups

    with open(os.path.join("experiments", "profiles.json"), "w") as f:
        json.dump({"profiles": [p.model_dump() for p in profiles]}, f)


if __name__ == "__main__":
    asyncio.run(main())
