(() => {
  const panel = document.querySelector(".aaditech-chatbot__panel");
  const toggle = document.querySelector(".aaditech-chatbot__toggle");
  const closeBtn = document.querySelector(".aaditech-chatbot__close");
  const body = document.querySelector(".aaditech-chatbot__body");
  const input = document.querySelector(".aaditech-chatbot__input");
  const sendBtn = document.querySelector(".aaditech-chatbot__send");

  if (!panel || !toggle || !body || !input || !sendBtn) {
    return;
  }

  const history = [];
  let lastTrigger = null;

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

  const scrollToLatest = () => {
    body.scrollTop = body.scrollHeight;
  };

  const addMessage = (text, role) => {
    const wrapper = document.createElement("div");
    wrapper.className = `aaditech-chatbot__message aaditech-chatbot__message--${role}`;

    const bubble = document.createElement("div");
    bubble.className = "aaditech-chatbot__bubble";
    bubble.textContent = text;

    wrapper.appendChild(bubble);
    body.appendChild(wrapper);
    scrollToLatest();
  };

  const setPending = (isPending) => {
    sendBtn.disabled = isPending;
    input.disabled = isPending;
    sendBtn.textContent = isPending ? "..." : "Send";
    panel.setAttribute("aria-busy", isPending ? "true" : "false");
  };

  const setOpen = (isOpen, trigger) => {
    if (isOpen && trigger) {
      lastTrigger = trigger;
    }

    panel.classList.toggle("is-open", isOpen);
    panel.setAttribute("aria-hidden", isOpen ? "false" : "true");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");

    if (isOpen) {
      requestAnimationFrame(() => {
        input.focus();
        scrollToLatest();
      });
      return;
    }

    if (lastTrigger && typeof lastTrigger.focus === "function") {
      lastTrigger.focus();
    } else {
      toggle.focus();
    }
  };

  const api = {
    open(trigger = null) {
      setOpen(true, trigger);
    },
    close() {
      setOpen(false);
    },
    toggle(trigger = null) {
      setOpen(!panel.classList.contains("is-open"), trigger);
    },
    isOpen() {
      return panel.classList.contains("is-open");
    },
  };

  const sendMessage = async () => {
    const text = input.value.trim();
    if (!text || sendBtn.disabled) return;

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
          history: history.slice(-8),
        }),
      });

      let data = {};
      try {
        data = await resp.json();
      } catch (error) {
        data = {};
      }

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

  window.AaditechChatbot = api;

  toggle.addEventListener("click", () => {
    api.toggle(toggle);
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      api.close();
    });
  }

  sendBtn.addEventListener("click", sendMessage);

  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && api.isOpen()) {
      api.close();
    }
  });

  document.addEventListener("aaditech:chatbot-open", (event) => {
    api.open(event.detail?.trigger || null);
  });

  document.addEventListener("aaditech:chatbot-close", () => {
    api.close();
  });

  panel.setAttribute("aria-hidden", "true");

  if (!body.children.length) {
    addMessage("Hi, I am AaDiTeCh. How can I help you today?", "bot");
  }
})();
