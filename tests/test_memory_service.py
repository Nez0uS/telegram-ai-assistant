from services import MemoryService


def test_history_limit():
    memory_service = MemoryService()
    user_id = 123

    for i in range(21):
        memory_service.add_message(
            user_id,
            "user",
            f"Привет{i}"
        )

    messages = memory_service.get_messages(user_id)

    assert len(messages) == 20
    assert messages[0]["content"] == "Привет1"
    assert messages[-1]["content"] == "Привет20"

def test_users_have_separate_history():
    memory_service = MemoryService()

    memory_service.add_message(1, "user", "Привет от первого")
    memory_service.add_message(2, "user", "Привет от второго")

    user_1_messages = memory_service.get_messages(1)
    user_2_messages = memory_service.get_messages(2)

    assert user_1_messages == [
        {"role": "user", "content": "Привет от первого"}
    ]

    assert user_2_messages == [
        {"role": "user", "content": "Привет от второго"}
    ]

def test_clear_history():
    memory_service = MemoryService()
    user_id = 123

    memory_service.add_message(user_id, "user", "Привет")
    memory_service.add_message(user_id, "assistant", "Здравствуйте!")

    memory_service.clear_history(user_id)
    messages = memory_service.get_messages(user_id)

    assert messages == []
