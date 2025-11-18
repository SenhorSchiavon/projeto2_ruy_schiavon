from constants import TEMPO_MAX_300, BARRA_FIXA_MIN, TEMPO_MAX_2400

class BaseValidationHandler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, candidate):
        if self.next_handler:
            return self.next_handler.handle(candidate)
        return candidate

class Corrida300Handler(BaseValidationHandler):
    def handle(self, candidate):
        tempo = candidate.get("tempo_300")
        if tempo is None or tempo > TEMPO_MAX_300:
            candidate["status"] = "REPROVADO"
        return super().handle(candidate)

class BarraFixaHandler(BaseValidationHandler):
    def handle(self, candidate):
        repeticoes = candidate.get("barra_fixa")
        if repeticoes is None or repeticoes < BARRA_FIXA_MIN:
            candidate["status"] = "REPROVADO"
        return super().handle(candidate)

class Corrida2400Handler(BaseValidationHandler):
    def handle(self, candidate):
        tempo = candidate.get("tempo_2400")
        if tempo is None or tempo > TEMPO_MAX_2400:
            candidate["status"] = "REPROVADO"
        return super().handle(candidate)

class ResultadoFinalHandler(BaseValidationHandler):
    def handle(self, candidate):
        if "status" not in candidate:
            candidate["status"] = "APROVADO"
        return super().handle(candidate)
