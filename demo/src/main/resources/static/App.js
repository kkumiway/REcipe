// 채팅 메시지를 표시할 DOM
const chatMessages = document.querySelector('#chat-messages');
// 사용자 입력 필드
const userInput = document.querySelector('#user-input input');
// 전송 버튼
const sendButton = document.querySelector('#user-input button');

window.onload = function() {
    // 첫 번째 챗봇 메시지
    const firstMessage = "안녕하세요! 저는 RE:cipe예요. 어떤 재료가 있는지 알려주시면, 그 재료로 만들 수 있는 맛있는 레시피를 추천해 드릴게요!";

    const profilePic = document.createElement('img');
    profilePic.className = 'profile-pic bot';
    profilePic.src = "/src/main/resources/static/assets/profile-bot.png";

    // 메시지 HTML 생성
    const chatMessages = document.getElementById('chat-messages');
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container');

    const botMessage = document.createElement('div');
    botMessage.classList.add('message', 'bot');
    botMessage.innerText = firstMessage;

    // 메시지 컨테이너에 추가
    messageContainer.appendChild(profilePic);
    messageContainer.appendChild(botMessage);
    chatMessages.appendChild(messageContainer);

    // 스크롤을 맨 아래로 이동
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

// 사용자 메시지를 화면에 추가하는 함수
function addMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message-container';

    // 프로필 사진 추가
    const profilePic = document.createElement('img');
    profilePic.className = 'profile-pic ' + (sender === '나' ? 'user' : 'bot');
    profilePic.src = sender === '나' ? '/src/main/resources/static/assets/profile-user.png' : '/src/main/resources/static/assets/profile-bot.png';

    // 메시지 박스 생성
    const messageText = document.createElement('span');
    messageText.className = 'message ' + (sender === '나' ? 'user' : 'bot');
    messageText.textContent = message;

    // 메시지 컨테이너에 추가
    messageElement.appendChild(profilePic);
    messageElement.appendChild(messageText);
    chatMessages.appendChild(messageElement);

    // 스크롤을 맨 아래로 이동
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ✅ OpenAI API를 직접 호출하지 않고, 백엔드에 요청을 보내는 함수
async function sendMessageToServer(userInput) {
    try {
        const response = await fetch('/bot/chat', {  // 백엔드(Spring Boot) 엔드포인트 호출
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userInput })  // JSON 형식으로 사용자 입력 전송
        });

        if (!response.ok) {
            console.error("API 요청 실패:", response.statusText);
            return "죄송합니다. 응답을 받을 수 없습니다.";
        }

        const data = await response.json();
        return data.response;  // 백엔드 응답(JSON)에서 `response` 필드 값 반환
    } catch (error) {
        console.error('API 호출 중 오류 발생:', error);
        return 'API 호출 중 오류 발생';
    }
}

// ✅ 전송 버튼 클릭 이벤트 처리
sendButton.addEventListener('click', async () => {
    const message = userInput.value.trim();
    if (message.length === 0) return;

    addMessage('나', message);
    userInput.value = '';

    const aiResponse = await sendMessageToServer(message);  // 백엔드(Spring Boot) 호출
    addMessage('챗봇', aiResponse);
});

// ✅ 사용자 입력 필드에서 Enter 키 입력 처리
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});
