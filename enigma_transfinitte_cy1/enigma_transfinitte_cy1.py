import reflex as rx
from .response import model
from .gitfiles import git_repository


class ChatState(rx.State):
    request: str
    response: str
    chat_history: list[tuple[bool, str]] = []
    is_user: bool = True
    processing: bool = True

    def handle_submit(self, data: dict):
        self.request = data["prompt"]
        if not self.request.strip():
            return

        self.chat_history.append((self.is_user, self.request))
        self.get_response()

    def set_response(self, new):
        self.response = new

    def toggle_processing(self):
        self.processing = not self.processing

    def get_response(self):
        try:
            response = model.generate_content(
                [
                    """From the given input:
                      if the input has any sort of programming language code in it,
                        then = (return a tuple with '1' and the code eg. ('1', 'print("Hello World")'))
                      else if the input has a github respository link,
                        then = (return the tuple '2' and the github link eg. ('2', 'https://github.com/username/repository'))
                      else,
                        then = (Forget all conditions and act like a normal chatbot and reply to the user)
                        \n
                    """,
                    str(self.request),
                ],
            )
            self.response = eval(response.text)
            match int(self.response[0]):
                case 1:
                    self.response = model.generate_content(
                        [
                            "You are an application security testing tool. I am going to provide you with a code. Point out exactly what my vulnerabilities are, and mention the level of danger of the vulnerability, show the exact lines where the specific vulnerability is found, and finally generate the lines of code without the vulnerability\n\n",
                            str(self.response[1]),
                        ],
                    ).text

                case 2:
                    code = git_repository(str(self.response[1]))
                    self.response = model.generate_content(
                        [
                            "You are an application security testing tool. I am going to provide you with code from a github repository, with each file name. Point out exactly what my vulnerabilities are, and which file they are in, and mention the level of danger of the vulnerability, show the exact lines where the specific vulnerability is found\n\n",
                            code,
                        ],
                    ).text

                case _:
                    self.response = "There was an error in processing the request. Please try again later."

        except:
            pass
        self.chat_history.append((not self.is_user, self.response))

    def clear_history(self):
        self.chat_history = []


def textbubble(is_user: bool, req: str = "", res: str = "") -> rx.Component:
    return rx.flex(
        rx.cond(
            is_user,
            rx.hstack(
                rx.text(
                    req,
                    padding_inline="10px",
                    padding_block="5px",
                    background_color="#6e56cf",
                    border_radius="12px",
                    max_width="750px",
                    font_family="Instrument Sans",
                ),
                rx.image(
                    "user.png",
                    width="32px",
                    height="32px",
                ),
            ),
            rx.hstack(
                rx.image(
                    "ai.png",
                    width="32px",
                    height="32px",
                ),
                rx.markdown(
                    res,
                    padding_inline="10px",
                    padding_block="5px",
                    background_color="#1f1f1f",
                    border_radius="12px",
                    max_width="750px",
                    font_family="Instrument Sans",
                ),
            ),
        ),
        direction="row-reverse" if is_user else "row",
    )


def chatbox() -> rx.Component:
    return rx.flex(
        rx.scroll_area(
            rx.flex(
                rx.foreach(
                    ChatState.chat_history,
                    lambda chat: rx.cond(
                        chat[0],
                        textbubble(True, req=chat[1]),
                        textbubble(False, res=chat[1]),
                    ),
                ),
                padding="15px",
                direction="column",
                spacing="4",
            ),
            type="hover",
            scrollbars="vertical",
        ),
        rx.form.root(
            rx.hstack(
                rx.text_area(
                    placeholder="Ask anything",
                    name="prompt",
                    variant="soft",
                    radius="full",
                    height="50px",
                    class_name="relative w-full",
                    padding_inline="5px",
                ),
                rx.button(
                    rx.cond(
                        ChatState.processing,
                        rx.icon(
                            "arrow_up",
                            on_click=ChatState.toggle_processing,
                        ),
                        rx.spinner(),
                    ),
                ),
                rx.icon_button(
                    "trash-2",
                    on_click=ChatState.clear_history,
                    disabled=~ChatState.chat_history,
                ),
                align="center",
            ),
            on_submit=ChatState.handle_submit,
            reset_on_submit=True,
        ),
        background_image="url('Background.png')",
        background_size="cover",
        spacing="3",
        direction="column",
        padding="15px",
        border="3px solid #43474e",
        border_radius="12px",
        height="600px",
        width="1100px",
    )


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.spacer(),
            rx.heading(
                "Welcome to CAAST.ai",
                size="9",
                font_family="Instrument Sans",
            ),
            rx.divider(),
            rx.text(
                "Code Analyser and Application Security Testing Tool is an intelligent LLM based chatbot capable of accepting code in different languages which identifies potential vulnerabilities in your code along with its fixes",
                size="4",
                font_family="Instrument Sans",
            ),
            chatbox(),
            align="center",
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        background_image="url('main_background.png')",
        background_size="cover",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap",
    ],
    theme=rx.theme(
        appearance="dark",
        accent_color="violet",
    ),
)
app.add_page(index)
