from aiogram.dispatcher.filters.state import StatesGroup, State


class IniciatorStates(StatesGroup):
    #
    State1 = State()
    #
    State2 = State()
    #
    State3 = State()
    #
    State4 = State()
    #
    State5 = State()
    #
    State6 = State()


class AdminStates(StatesGroup):
    EnterName = State()


class Chatting(StatesGroup):
    ToAdmin = State()
    ToPI = State()
