// 채팅 메시지를 표시할 DOM
const chatMessages = document.querySelector('#chat-messages');
// 사용자 입력 필드
const userInput = document.querySelector('#user-input input');
// 전송 버튼
const sendButton = document.querySelector('#user-input button');

// 발급받은 OpenAI API 키를 변수로 저장
const apiKey = '발급받은 API키 입력';
// OpenAI API 엔드포인트 주소를 변수로 저장
const apiEndpoint = 'https://api.openai.com/v1/chat/completions'

window.onload = function() {
    // 첫 번째 챗봇 메시지
    const firstMessage = "안녕하세요! 저는 RE:cipe예요. 어떤 재료가 있는지 알려주시면, 그 재료로 만들 수 있는 맛있는 레시피를 추천해 드릴게요!";

    const profilePic = document.createElement('img');
    profilePic.className = 'profile-pic bot';
    profilePic.src = '../assets/profile-bot.png';  // 사용자와 챗봇의 프로필 사진을 구분

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

    // 메시지 출력 후 스크롤을 맨 아래로 이동
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

function addMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message-container';

    // 프로필 사진 추가
    const profilePic = document.createElement('img');
    profilePic.className = 'profile-pic '+ (sender === '나' ? 'user' : 'bot');
    profilePic.src = sender === '나' ? '../assets/profile-user.png' : '../assets/profile-bot.png';  // 사용자와 챗봇의 프로필 사진을 구분

    // 새로운 div 생성 (메시지의 전체 컨테이너)
    const messageText = document.createElement('span');
    // 생성된 요소에 클래스 추가
    messageText.className = 'message ' + (sender === '나' ? 'user' : 'bot');
    messageText.textContent = message;

    // 프로필 사진과 메시지를 포함하는 div에 추가
    messageElement.appendChild(profilePic);
    messageElement.appendChild(messageText);
    
    chatMessages.prepend(messageElement);
}


// ChatGPT API 요청
async function fetchAIResponse(prompt) {
    // API 요청에 사용할 옵션을 정의
    const requestOptions = {
        method: 'POST',
        // API 요청의 헤더를 설정
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",  // 사용할 AI 모델
            messages: [{
                role: "user", // 메시지 역할을 user로 설정
                content: prompt // 사용자가 입력한 메시지
            }, ],
            temperature: 0.8, // 모델의 출력 다양성
            max_tokens: 1024, // 응답받을 메시지 최대 토큰(단어) 수 설정
            top_p: 1, // 토큰 샘플링 확률을 설정
            frequency_penalty: 0.5, // 일반적으로 나오지 않는 단어를 억제하는 정도
            presence_penalty: 0.5, // 동일한 단어나 구문이 반복되는 것을 억제하는 정도
            stop: ["Human"], // 생성된 텍스트에서 종료 구문을 설정
        }),
    };
    // API 요청후 응답 처리
    try {
        const response = await fetch(apiEndpoint, requestOptions);
        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        return aiResponse;
    } catch (error) {
		console.error('OpenAI API 호출 중 오류 발생:', error);
        return 'OpenAI API 호출 중 오류 발생';
    }
}

// 전송 버튼 클릭 이벤트 처리
sendButton.addEventListener('click', async () => {
    // 사용자가 입력한 메시지
    const message = userInput.value.trim();
    // 메시지가 비어있으면 리턴
    if (message.length === 0) return;
    // 사용자 메시지 화면에 추가
    addMessage('나', message);
    userInput.value = '';
    //ChatGPT API 요청후 답변을 화면에 추가
    const aiResponse = await fetchAIResponse(message);
    addMessage('챗봇', aiResponse);
});

// 사용자 입력 필드에서 Enter 키 이벤트를 처리
userInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        sendButton.click();
    }
});