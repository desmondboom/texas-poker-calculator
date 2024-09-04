from typing import List

from src.game.evaluator.strategy.default_strategy import DefaultHandRankingEvaluateStrategy
from src.game.evaluator.strategy.strategy import HandRankingEvaluateStrategy


def error_message_with_strategy(test_desc: str, strategy: HandRankingEvaluateStrategy) -> str:
    return f"Failed test: {test_desc} with {strategy.__class__.__name__}"


def get_strategies() -> List[HandRankingEvaluateStrategy]:
    return [
        DefaultHandRankingEvaluateStrategy(),
    ]
