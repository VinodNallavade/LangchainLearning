from langchain_core.prompts import PromptTemplate



template = PromptTemplate(
            template= """
            Start with Thanks for using the Travel World then,
            Create a travel plan for someone visiting {city_name}, 
            interested in {interest},
            staying for {stay_duration} days, 
            and having a {budget} budget.
            Don't ask for more information. Just provide the travel plan and Avoid asking for printing or format change or any other things.
            """,
            input_variables=["city_name", "interest", "stay_duration", "budget"],
            validate_template=True

            ) 


template.save("./prompt_generator.json")