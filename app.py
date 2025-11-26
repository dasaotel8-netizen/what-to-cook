import streamlit as st
from PIL import Image
from openai import OpenAI

client = OpenAI()

st.title("🍽️ Что приготовить? — ИИ подскажет!")

uploaded_image = st.file_uploader("Загрузите фото продуктов", type=["jpg", "png"])
text_products = st.text_area("Или введите продукты вручную:")

def analyze_image(image_bytes):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": [
                {"type": "input_text", "text": "Что находится на фото? Назови только продукты."},
                {"type": "input_image", "image_url": image_bytes}
            ]}
        ]
    )
    return response.choices[0].message["content"]

def generate_recipes(products):
    prompt = f"""
Дано: {products}.
Составь 3–5 рецептов. Для каждого дай:
- название
- время приготовления
- список ингредиентов
- пошаговый рецепт
- калорийность (если возможно)
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

if st.button("Получить рецепты"):

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Загруженное фото")

        img_bytes = uploaded_image.getvalue()
        products = analyze_image(img_bytes)
        st.write("Обнаруженные продукты:", products)

    else:
        products = text_products

    st.subheader("🍳 Возможные блюда:")
    recipes = generate_recipes(products)
    st.write(recipes)
