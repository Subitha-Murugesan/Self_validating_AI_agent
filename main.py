import os
import json
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import openai
import install_requirements


class FeedbackSummaryGenerator:
    def __init__(self, max_iterations=5):
        try:
            # Load environment variables
            load_dotenv()
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")

            self.max_iterations = max_iterations

            # Initialize OpenAI API key
            openai.api_key = self.openai_api_key

            # Load pre-trained sentence embedding model
            self.model = SentenceTransformer('all-MiniLM-L6-v2')

            # Install required packages
            install_requirements.install_requirements()
        except Exception as error:
            print(f"Error during initialization: {error}")
            raise

    def generate_summary(self, feedback):
        """Generate an initial summary using GPT-3.5 turbo."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates summaries for customer feedback."},
                    {"role": "user", "content": f"Summarize the following feedback: {feedback}"}
                ],
                max_tokens=150
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.OpenAIError as error:
            print(f"OpenAI API error while generating summary: {error}")
            return "Error: Unable to generate summary due to OpenAI API issues."
        except Exception as error:
            print(f"Unexpected error while generating summary: {error}")
            return "Error: An unexpected issue occurred while generating the summary."

    def validate_relevance_and_consistency(self, summary, original_text):
        """Validate summary relevance and consistency using cosine similarity."""
        try:
            # Compute sentence embeddings for both the summary and original text
            summary_embedding = self.model.encode([summary])
            original_text_embedding = self.model.encode([original_text])

            # Compute cosine similarity between the embeddings
            similarity = cosine_similarity(summary_embedding, original_text_embedding)[0][0]

            # Classify relevance and consistency based on similarity score
            if similarity > 0.85:  # High similarity (closer to 1)
                confidence = "High"
            elif similarity > 0.5:  # Moderate similarity
                confidence = "Medium"
            else:  # Low similarity (closer to 0)
                confidence = "Low"

            return confidence, similarity
        except ValueError as error:
            print(f"Error while computing similarity: {error}")
            return "Error", 0
        except Exception as error:
            print(f"Unexpected error during validation: {error}")
            return "Error", 0

    def improve_summary(self, feedback, previous_summary):
        """Refine the summary based on feedback."""
        try:
            refined_summary = self.generate_summary(
                f"{feedback} (Make the summary more accurate, focused, and detailed.)"
            )
            return refined_summary
        except Exception as error:
            print(f"Error while refining summary: {error}")
            return "Error: Unable to refine the summary."

    def process_feedback(self, feedback_data):
        """Process feedback entries and refine summaries based on the iterative process."""
        for entry in feedback_data:
            try:
                feedback = entry["feedback"]
                print(f"Processing feedback for ID: {entry['id']}")

                # Step 1: Generate initial summary
                summary = self.generate_summary(feedback)
                print(f"Initial Summary: {summary}")

                # Step 2: Validate the summary for accuracy, relevance, and consistency
                confidence, similarity = self.validate_relevance_and_consistency(summary, feedback)
                print(f"\nConfidence: {confidence}")
                print(f"Similarity Score: {similarity}")

                # Iterative improvement process
                iteration = 0
                while iteration < self.max_iterations:
                    if similarity < 0.8:  # Low similarity (closer to 0)
                        print(f"\nRefining summary (Iteration {iteration + 1})...")

                        # Refine the summary based on feedback
                        refined_summary = self.improve_summary(feedback, summary)
                        print(f"\nRefined Summary: {refined_summary}")

                        # Revalidate the refined summary
                        confidence, similarity = self.validate_relevance_and_consistency(refined_summary, feedback)
                        print(f"\nNew Confidence: {confidence}")
                        print(f"New Similarity Score: {similarity}")

                        # If similarity is still low, stop the iteration and further proceed with RLHF using human feedback
                        if similarity < 0.8 and iteration == self.max_iterations - 1:
                            print("\nSummary refinement failed to improve sufficiently. Human feedback needed.")
                            break

                    iteration += 1
                    if similarity >= 0.8:
                        print("\nSummary is now acceptable.")
                        break

                print("\n" + "-" * 50)

            except KeyError as error:
                print(f"Missing key in feedback entry: {error}")
            except Exception as error:
                print(f"Unexpected error while processing feedback ID {entry['id']}: {error}")


if __name__ == "__main__":
    try:
        # Load input data from a JSON file
        with open(r'feedback_data.json', 'r') as f:
            input_data = json.load(f)

        # Initialize the FeedbackSummaryGenerator class
        feedback_summary_generator = FeedbackSummaryGenerator()

        # Process feedback data
        feedback_summary_generator.process_feedback(input_data)
    except FileNotFoundError as error:
        print(f"Feedback data file not found: {error}")
    except json.JSONDecodeError as error:
        print(f"Error parsing JSON file: {error}")
    except Exception as error:
        print(f"Unexpected error in main program: {error}")
