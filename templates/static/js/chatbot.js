(() => {
  const panel = document.querySelector(".aaditech-chatbot__panel");
  const toggle = document.querySelector(".aaditech-chatbot__toggle");
  const body = document.querySelector(".aaditech-chatbot__body");
  const input = document.querySelector(".aaditech-chatbot__input");
  const sendBtn = document.querySelector(".aaditech-chatbot__send");

  if (!panel || !toggle || !body || !input || !sendBtn) {
    return;
  }

  const history = [];

  const getMetaToken = () => {
    const meta = document.querySelector("meta[name='csrf-token']");
    return meta ? meta.getAttribute("content") : "";
  };

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
      return parts.pop().split(";").shift();
    }
    return "";
  };

  const addMessage = (text, role) => {
    const wrapper = document.createElement("div");
    wrapper.className = `aaditech-chatbot__message aaditech-chatbot__message--${role}`;
    const bubble = document.createElement("div");
    bubble.className = "aaditech-chatbot__bubble";
    bubble.textContent = text;
    wrapper.appendChild(bubble);
    body.appendChild(wrapper);
    body.scrollTop = body.scrollHeight;
  };

  const setPending = (isPending) => {
    sendBtn.disabled = isPending;
    input.disabled = isPending;
    sendBtn.textContent = isPending ? "..." : "Send";
  };

  const sendMessage = async () => {
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    addMessage(text, "user");
    history.push({ role: "user", content: text });
    setPending(true);

    try {
      const resp = await fetch("/api/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getMetaToken() || getCookie("csrftoken"),
        },
        body: JSON.stringify({
          message: text,
          history: history.slice(-6),
        }),
      });
      const data = await resp.json();
      if (!resp.ok || !data.reply) {
        throw new Error(data.error || "AI error");
      }
      addMessage(data.reply, "bot");
      history.push({ role: "assistant", content: data.reply });
    } catch (err) {
      addMessage("Sorry, AaDiTeCh is not available right now.", "bot");
    } finally {
      setPending(false);
    }
  };

  toggle.addEventListener("click", () => {
    panel.classList.toggle("is-open");
  });

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  });

  addMessage("Hi, I am AaDiTeCh. How can I help you today?", "bot");
})();
