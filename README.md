# Lesson Plan Roadmap Generator

Generate personalized learning roadmaps with the help of AI. This project leverages the power of machine learning to tailor educational pathways based on your interests and goals.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have a working installation of Python 3.8 or newer.
- You have an OpenAI API key. This key needs to be included within a `.env` file at the root of this project.

## Setting Up Your Environment

1. **Clone the Repository**

   Start by cloning this repository to your local machine:

   ```bash
   git clone https://github.com/yeo-menghan/roadmap_gen.git
   cd roadmap_gen
   ```
2. **Configure Environment Variables**
    Create a .env file in the root directory of the project and add your OpenAI API key as follows:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```
3. **Install Dependencies**
    Install the required Python packages using pip:
    ```
    pip install -r requirements.txt
    ```

## Running the Project

    To generate the json output of the roadmap, utilise the following script:
    ```
    python main.py
    ```

## Experimenting with the code
    For those interested in diving deeper into the project's workings, the iterate_topic.ipynb Jupyter Notebook is available. This notebook allows for hands-on experimentation with the code, offering insights into the logic and methodology behind the roadmap generation process.

    To use the notebook, ensure you have Jupyter installed, then run the code blocks within the notebook on a code editor tool like vscode.

## Contact
    Name: Yeo Meng Han
    Project Link: https://github.com/yeo-menghan/roadmap_gen
