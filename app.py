import openai
import re
import time

import os
openai.api_key = os.getenv("OPENAI_API_KEY")
# Step 1: Generate the story


def generate_story(data):
    record = data['record']
    child_name = record['full_name']
    favorite_interests = record['hobbies']
    condition = record['diagnosis']
    starting_location = record['city']
    resolution = record.get('resolution', 'a comforting resolution')

    story_prompt = f"""
    You will now act as the Care Tales chatbot, assisting in the process of writing custom children's 
    books for children with chronic and serious illnesses. The book you will be creating will be a 19-
    page book for {child_name}, who loves {favorite_interests}. The story should help 
    [him/her/them] navigate {condition} in a way that is empowering, educational, and uplifting. 
    Start the story in {starting_location}, and conclude it with {resolution}. Now create the 
    story for the 19 page picture book. Include a description of the illustration that coincides with 
    each page.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": story_prompt}
        ]
    )

    response_message = completion['choices'][0]['message']['content']
    return response_message

# Step 2: Split the story into pages


def split_story_into_pages(story):
    pages = story.split('Page')  # Split by 'Page' delimiter
    return pages

# Step 3: Generate detailed prompt for image generation ensuring consistency


def generate_image_for_page(page_story):
    # Try to extract the illustration description
    match = re.search(r'\[Illustration:(.*?)\]', page_story, re.DOTALL)

    if match:
        # Extract only the illustration description
        illustration_description = match.group(1).strip()
    else:
        # Fallback if no illustration description is found
        illustration_description = "A scene that fits the narrative of the page."

    # Ensure the prompt is under 1000 characters
    if len(illustration_description) > 1000:
        # Trim if necessary
        illustration_description = illustration_description[:1000]

    # Custom GPT instructions for generating consistent images with the same boy's face
    image_prompt = (
        f"Create a 3D Pixar animation style illustration of the following scene: {illustration_description}. "
        "Subject Description: The main character is John, a 9-year-old half-Mexican, half-Caucasian boy with curly dark brown hair, "
        "wearing a red hoodie, holding a badminton racket, and always having a cheerful smile. "
        "The boy's face, features, and appearance must remain consistent across all images to ensure character uniformity. "
        "Environment Description: The background is consistent with the story, featuring relevant environmental details. "
        "Art Style: 3D Pixar animation style. "
        "Color and Light: Warm colors and natural lighting to create a cheerful and engaging mood. "
        "Camera Angle and Composition: A cinematic perspective with a focus on the main subject."
        "Try to keep the photo of teh consistent throug the whole story and not changess in his face structure etc."
    )

    # Send the custom prompt to OpenAI for image generation
    dalle_response = openai.Image.create(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024"  # Larger size for better quality
    )

    image_url = dalle_response['data'][0]['url']
    print(illustration_description)
    print(f"Image URL for page: {image_url}")
    return image_url

# Step 4: Upload the image to knowledge (this is a placeholder)


def upload_image_to_knowledge(image_url, page_number):
    print(f"Uploading Page {page_number}'s image to knowledge: {image_url}")
    # Implement actual upload logic here

# Step 5: Iterate through each page and generate images


def process_story_and_generate_images(story):
    pages = split_story_into_pages(story)
    all_images = []

    for i, page in enumerate(pages[1:]):  # Ignore first split (empty) entry
        page_story = page.strip()  # Clean up whitespace
        print(f"Processing Page {i+1}")

        # Step 3: Generate image for the current page
        image_url = generate_image_for_page(page_story)
        all_images.append(image_url)
        time.sleep(30)  # Delay to avoid hitting rate limits
        # Step 4: Upload image to knowledge
        # upload_image_to_knowledge(image_url, i+1)

    return all_images

# Step 6: The main function to execute the whole process


def main():
    # Example data input
    data = {
        'record': {
            'full_name': 'John',
            'hobbies': 'badminton',
            'diagnosis': 'asthma',
            'city': 'Ohio'
        }
    }

    # Step 1: Generate the story
    story = generate_story(data)
    # Step 5: Process the story, generate images, and upload them
    all_images = process_story_and_generate_images(story)

    # Step 6: Return all generated images
    return all_images


# Run the process
final_images = main()
print(final_images)