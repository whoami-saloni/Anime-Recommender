from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY,MODEL_NAME
from utils.logger import get_logger
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommendationPipeline:
    def __init__(self,persist_dir="chroma_db"):
        try:
            logger.info("Initializing VectorStoreBuilder...")
            vector_builder = VectorStoreBuilder(csv_path="", persist_dir=persist_dir)
            retriever=vector_builder.load_vectorstore().as_retriever()
            self.recommender = AnimeRecommender(
                retriever=retriever,
                api_key=GROQ_API_KEY,
                model_name=MODEL_NAME
            )
            logger.info("Pipeline initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing Pipeline: {e}")
            raise CustomException(e)
        
    def recommend(self,query:str):
        try:
            logger.info(f"Received a query: {query}")
            recommendation = self.recommender.get_recommendation(query)
            logger.info("Recommendation generated successfully.")
            return recommendation
        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            raise CustomException(e)
