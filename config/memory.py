from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

#Short-term memory configuration
checkpointer= InMemorySaver()

#Long-term memory configuration
store = InMemoryStore()
