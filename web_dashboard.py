"""
Веб-панель для просмотра статистики бота
"""
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json

from models import db_manager, ChatInteraction
from config import config

app = Flask(__name__)


class DashboardService:
    """Сервис для получения данных для панели управления"""
    
    @staticmethod
    def get_overview_stats() -> Dict[str, Any]:
        """Получает общую статистику"""
        session = db_manager.get_session()
        try:
            total_interactions = session.query(ChatInteraction).count()
            responses_generated = session.query(ChatInteraction)\
                .filter(ChatInteraction.response_generated == True).count()
            
            unique_chats = session.query(ChatInteraction.chat_id).distinct().count()
            
            # Статистика за последние 24 часа
            yesterday = datetime.utcnow() - timedelta(days=1)
            recent_interactions = session.query(ChatInteraction)\
                .filter(ChatInteraction.timestamp >= yesterday).count()
            
            # Соотношение настроений
            sentiments = session.query(ChatInteraction.sentiment).all()
            sentiment_counts = {
                'positive': 0,
                'neutral': 0,
                'negative': 0
            }
            
            for sentiment_row in sentiments:
                sentiment = sentiment_row[0]
                if sentiment in sentiment_counts:
                    sentiment_counts[sentiment] += 1
            
            return {
                'total_interactions': total_interactions,
                'responses_generated': responses_generated,
                'unique_chats': unique_chats,
                'recent_interactions': recent_interactions,
                'response_rate': responses_generated / max(total_interactions, 1) * 100,
                'sentiment_distribution': sentiment_counts
            }
        finally:
            session.close()
    
    @staticmethod
    def get_chat_list() -> List[Dict[str, Any]]:
        """Получает список чатов с статистикой"""
        session = db_manager.get_session()
        try:
            # Группируем по чатам
            chats_data = session.query(
                ChatInteraction.chat_id,
                ChatInteraction.chat_title
            ).distinct().all()
            
            result = []
            for chat_id, chat_title in chats_data:
                chat_interactions = session.query(ChatInteraction)\
                    .filter(ChatInteraction.chat_id == chat_id).count()
                
                chat_responses = session.query(ChatInteraction)\
                    .filter(ChatInteraction.chat_id == chat_id)\
                    .filter(ChatInteraction.response_generated == True).count()
                
                # Последнее взаимодействие
                last_interaction = session.query(ChatInteraction)\
                    .filter(ChatInteraction.chat_id == chat_id)\
                    .order_by(ChatInteraction.timestamp.desc())\
                    .first()
                
                result.append({
                    'chat_id': chat_id,
                    'chat_title': chat_title or 'Неизвестный чат',
                    'total_interactions': chat_interactions,
                    'responses_generated': chat_responses,
                    'response_rate': chat_responses / max(chat_interactions, 1) * 100,
                    'last_activity': last_interaction.timestamp.isoformat() if last_interaction else None
                })
            
            return sorted(result, key=lambda x: x['total_interactions'], reverse=True)
        finally:
            session.close()
    
    @staticmethod
    def get_recent_interactions(limit: int = 50) -> List[Dict[str, Any]]:
        """Получает последние взаимодействия"""
        session = db_manager.get_session()
        try:
            interactions = session.query(ChatInteraction)\
                .order_by(ChatInteraction.timestamp.desc())\
                .limit(limit).all()
            
            result = []
            for interaction in interactions:
                result.append({
                    'id': interaction.id,
                    'timestamp': interaction.timestamp.isoformat(),
                    'chat_title': interaction.chat_title,
                    'detected_topic': interaction.detected_topic,
                    'sentiment': interaction.sentiment,
                    'response_generated': interaction.response_generated,
                    'bot_response': interaction.bot_response[:100] + '...' if interaction.bot_response and len(interaction.bot_response) > 100 else interaction.bot_response,
                    'participants_count': interaction.participants_count
                })
            
            return result
        finally:
            session.close()


dashboard_service = DashboardService()


@app.route('/')
def index():
    """Главная страница дашборда"""
    return render_template('dashboard.html')


@app.route('/api/overview')
def api_overview():
    """API: Общая статистика"""
    try:
        stats = dashboard_service.get_overview_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chats')
def api_chats():
    """API: Список чатов"""
    try:
        chats = dashboard_service.get_chat_list()
        return jsonify(chats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/interactions')
def api_interactions():
    """API: Последние взаимодействия"""
    try:
        interactions = dashboard_service.get_recent_interactions()
        return jsonify(interactions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/bot-info')
def api_bot_info():
    """API: Информация о боте"""
    return jsonify({
        'bot_name': config.bot_name,
        'personality': config.bot_personality,
        'response_frequency': config.response_frequency,
        'min_context_messages': config.min_context_messages,
        'max_context_messages': config.max_context_messages
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 