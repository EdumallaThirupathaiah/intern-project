# # import streamlit as st

# # # Positive & Negative keywords
# # positive_words = ["good", "great", "excellent", "amazing", "happy", "love"]
# # negative_words = ["bad", "worst", "poor", "sad", "hate", "terrible"]

# # # Score function
# # def calculate_score(text):
# #     score = 0
# #     words = text.lower().split()

# #     for word in words:
# #         if word in positive_words:
# #             score += 1
# #         elif word in negative_words:
# #             score -= 1

# #     return score

# # # Sentiment function
# # def get_sentiment(score):
# #     if score > 0:
# #         return "Positive"
# #     elif score < 0:
# #         return "Negative"
# #     else:
# #         return "Neutral"

# # # UI
# # st.title("📊 Sentiment Analysis System")

# # user_input = st.text_area("Enter your review:")

# # if st.button("Analyze"):
# #     if user_input:
# #         score = calculate_score(user_input)
# #         sentiment = get_sentiment(score)

# #         st.success("Analysis Complete!")
# #         st.write("Score:", score)
# #         st.write("Sentiment:", sentiment)
# #     else:
# #         st.warning("Please enter some text!")
# import streamlit as st

# st.title("Sentiment Analysis Project")

# review = st.text_area("Enter your review")
# if st.button("Analyze"):
#      st.write("You entered:", review)