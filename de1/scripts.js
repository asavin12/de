document.addEventListener('DOMContentLoaded', () => {
    // Tùy chọn tĩnh cho Leseverstehen Teil 3
    const options = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'X'];

    // Mã hóa API keys (Base64)
    const encodedApiKeys = [
        'QUl6YVN5RHRuWng0U0RZcTQ0WmY2MVlPSnBndHhaVDhlT3dobzlJ', // Key 1
        'QUl6YVN5Q1hjT2pRcUlvX3FJVEgxY2k5SWUtdGU2alExRjJlR2Zv', // Key 2
        'QUl6YVN5Q2xUcjlBWFdGMVNycURFaVY2TzVCdzFBLVhTaURPOUdR'  // Key 3
    ].map(key => atob(key)); // Giải mã Base64 khi sử dụng

    // Cấu hình API
    const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash-lite:generateContent';
    const TIMEOUT_MS = 5000; // Timeout 5 giây
    let currentKeyIndex = 0; // Chỉ số key hiện tại
    const failedKeys = new Set(); // Lưu key thất bại
    const translationCache = new Map(); // Cache bản dịch

    // Tooltip cho bản dịch
    const translationTooltip = document.createElement('div');
    translationTooltip.id = 'translation-tooltip';
    translationTooltip.className = 'translation-tooltip';
    document.body.appendChild(translationTooltip);

    // Hàm gọi API với timeout
    async function fetchWithTimeout(url, options) {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), TIMEOUT_MS);
        try {
            const response = await fetch(url, { ...options, signal: controller.signal });
            clearTimeout(id);
            return response;
        } catch (error) {
            clearTimeout(id);
            throw error;
        }
    }

    // Hàm thử API với key hiện tại, chuyển key nếu lỗi
    async function tryTranslateWithKey(text) {
        if (failedKeys.size >= encodedApiKeys.length) {
            return 'Lỗi: Tất cả API key không khả dụng. Vui lòng thử lại sau.';
        }

        const apiKey = encodedApiKeys[currentKeyIndex];
        try {
            const response = await fetchWithTimeout(`${GEMINI_API_URL}?key=${apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: `Bạn là chuyên gia dịch thuật từ Tiếng Đức sang Tiếng Việt, vì vậy chỉ đưa ra nghĩa Tiếng Việt chính xác 1:1 như từ điển không giải thích gì thêm(có thể đưa ra thêm một vài nghĩa) cho từ Tiếng Đức "${text}"`
                        }]
                    }],
                    generationConfig: {
                        maxOutputTokens: 512,
                        temperature: 0.2 // Độ sáng tạo thấp để dịch sát nghĩa
                    }
                })
            });

            if (!response.ok) {
                if (response.status === 429) {
                    failedKeys.add(currentKeyIndex);
                    currentKeyIndex = (currentKeyIndex + 1) % encodedApiKeys.length;
                    return tryTranslateWithKey(text); // Thử key tiếp theo
                } else if (response.status === 401) {
                    failedKeys.add(currentKeyIndex);
                    currentKeyIndex = (currentKeyIndex + 1) % encodedApiKeys.length;
                    return tryTranslateWithKey(text); // Thử key tiếp theo nếu 401
                }
                throw new Error(`API error: ${response.statusText}`);
            }

            const data = await response.json();
            const translation = data.candidates[0].content.parts[0].text.trim();
            translationCache.set(text, translation); // Lưu cache
            return translation;
        } catch (error) {
            if (error.name === 'AbortError' || error.message.includes('network')) {
                failedKeys.add(currentKeyIndex);
                currentKeyIndex = (currentKeyIndex + 1) % encodedApiKeys.length;
                return tryTranslateWithKey(text); // Thử key tiếp theo
            }
            return `Lỗi: Không thể dịch (${error.message}).`;
        }
    }

    // Hàm dịch văn bản
    async function translateText(text) {
        if (text.length < 2) return '';
        // Kiểm tra cache
        if (translationCache.has(text)) {
            return translationCache.get(text);
        }
        return tryTranslateWithKey(text);
    }

    // Xử lý bôi đen văn bản
    document.addEventListener('mouseup', async (e) => {
        const selection = window.getSelection();
        const selectedText = selection.toString().trim();
        if (selectedText && selectedText.length >= 2) {
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            translationTooltip.style.top = `${rect.bottom + window.scrollY + 5}px`;
            translationTooltip.style.left = `${rect.left + window.scrollX}px`;
            translationTooltip.textContent = 'Đang dịch...';
            translationTooltip.style.display = 'block';

            const translation = await translateText(selectedText);
            translationTooltip.textContent = translation;
        } else {
            translationTooltip.style.display = 'none';
        }
    });

    // Ẩn tooltip khi click ra ngoài
    document.addEventListener('mousedown', (e) => {
        if (!translationTooltip.contains(e.target)) {
            translationTooltip.style.display = 'none';
        }
    });

    fetch('test.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Không thể tải test.json: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            // Leseverstehen Teil 1
            const teil1Div = document.getElementById('leseverstehen_teil1');
            data.leseverstehen_teil1.texts.forEach((text, index) => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question';
                questionDiv.innerHTML = `
                    <p class="font-medium"><span class="question-number">${index + 1}.</span> ${text.replace(/\r\n/g, '<br>')}</p>
                    <div class="option-grid">
                        ${data.leseverstehen_teil1.overschriften.map((opt, optIdx) => `
                            <label>
                                <input type="radio" name="teil1_${index}" value="${String.fromCharCode(65 + optIdx)}">
                                <strong>${String.fromCharCode(65 + optIdx)}</strong>. ${opt}
                            </label>
                        `).join('')}
                    </div>
                `;
                teil1Div.appendChild(questionDiv);
            });

            // Leseverstehen Teil 2
            const teil2ContentDiv = document.getElementById('leseverstehen_teil2_content');
            teil2ContentDiv.className = 'content';
            teil2ContentDiv.innerHTML = data.leseverstehen_teil2.content.replace(/\r\n/g, '<br>');
            const teil2QuestionsDiv = document.getElementById('leseverstehen_teil2_questions');
            data.leseverstehen_teil2.questions.forEach((question, index) => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question';
                questionDiv.innerHTML = `
                    <p class="font-medium"><span class="question-number">${index + 6}.</span> ${question}</p>
                    <div class="option-grid">
                        ${data.leseverstehen_teil2.options[index].map((opt, optIdx) => `
                            <label>
                                <input type="radio" name="teil2_${index}" value="${String.fromCharCode(65 + optIdx)}">
                                <strong>${String.fromCharCode(65 + optIdx)}</strong>. ${opt}
                            </label>
                        `).join('')}
                    </div>
                `;
                teil2QuestionsDiv.appendChild(questionDiv);
            });

            // Leseverstehen Teil 3
            const teil3Image = document.getElementById('leseverstehen_teil3_image');
            teil3Image.src = `/images/${data.leseverstehen_teil3.image_path.replace(/\\/g, '/').replace(/^\/+/, '').replace(/^images\//, '')}`;
            const teil3Div = document.getElementById('leseverstehen_teil3_situations');
            data.leseverstehen_teil3.situations.forEach((situation, index) => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question';
                questionDiv.innerHTML = `
                    <p class="font-medium"><span class="question-number">${index + 11}.</span> ${situation.replace(/\r\n/g, '<br>')}</p>
                    <select name="teil3_${index}" class="w-full sm:w-1/2 p-2 rounded">
                        <option value="">Chọn đáp án</option>
                        ${options.map(opt => `<option value="${opt}"><strong>${opt}</strong></option>`).join('')}
                    </select>
                `;
                teil3Div.appendChild(questionDiv);
            });

            // Sprachbausteine Teil 1
            const sprach1ContentDiv = document.getElementById('sprachbausteine_teil1_content');
            let content1 = data.sprachbausteine_teil1.content.replace(/\r\n/g, '<br>');
            for (let i = 21; i <= 30; i++) {
                content1 = content1.replace(`(${i})`, `<span id="sprach1_${i}"></span>(${i})`);
            }
            sprach1ContentDiv.className = 'content';
            sprach1ContentDiv.innerHTML = content1;
            const sprach1QuestionsDiv = document.getElementById('sprachbausteine_teil1_questions');
            data.sprachbausteine_teil1.options.forEach((opts, index) => {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question';
                questionDiv.innerHTML = `
                    <p class="font-medium"><span class="question-number">${index + 21}.</span></p>
                    <select name="sprach1_${index + 21}" class="w-full sm:w-1/2 p-2 rounded">
                        <option value="">Select an option</option>
                        ${opts.map((opt, optIdx) => `
                            <option value="${String.fromCharCode(97 + optIdx)}"><strong>${String.fromCharCode(65 + optIdx)}</strong>. ${opt}</option>
                        `).join('')}
                    </select>
                `;
                sprach1QuestionsDiv.appendChild(questionDiv);
            });

            // Sprachbausteine Teil 2
            const sprach2ContentDiv = document.getElementById('sprachbausteine_teil2_content');
            let content2 = data.sprachbausteine_teil2.content.replace(/\r\n/g, '<br>');
            for (let i = 31; i <= 40; i++) {
                content2 = content2.replace(`(${i})`, `<span id="sprach2_${i}"></span>(${i})`);
            }
            sprach2ContentDiv.className = 'content';
            sprach2ContentDiv.innerHTML = content2;
            const sprach2QuestionsDiv = document.getElementById('sprachbausteine_teil2_questions');
            for (let i = 31; i <= 40; i++) {
                const questionDiv = document.createElement('div');
                questionDiv.className = 'question';
                questionDiv.innerHTML = `
                    <p class="font-medium"><span class="question-number">${i}.</span></p>
                    <select name="sprach2_${i}" class="w-full sm:w-1/2 p-2 rounded">
                        <option value="">Select an option</option>
                        ${data.sprachbausteine_teil2.options.map((opt, optIdx) => `
                            <option value="${String.fromCharCode(65 + optIdx)}"><strong>${String.fromCharCode(65 + optIdx)}</strong>. ${opt}</option>
                        `).join('')}
                    </select>
                `;
                sprach2QuestionsDiv.appendChild(questionDiv);
            };

            // Kiểm tra đáp án
            document.getElementById('checkAnswers').addEventListener('click', () => {
                let score = 0;
                const totalQuestions = data.answers.length;
                const userAnswers = [];

                // Leseverstehen Teil 1
                for (let i = 0; i < data.leseverstehen_teil1.texts.length; i++) {
                    const selected = document.querySelector(`input[name="teil1_${i}"]:checked`);
                    const answer = selected ? selected.value : '';
                    userAnswers.push(answer);
                    const questionDiv = teil1Div.children[i];
                    if (answer === data.answers[i]) {
                        score++;
                        questionDiv.classList.add('correct');
                    } else {
                        questionDiv.classList.add('incorrect');
                    }
                }

                // Leseverstehen Teil 2
                for (let i = 0; i < data.leseverstehen_teil2.questions.length; i++) {
                    const selected = document.querySelector(`input[name="teil2_${i}"]:checked`);
                    const answer = selected ? selected.value : '';
                    userAnswers.push(answer);
                    const questionDiv = teil2QuestionsDiv.children[i];
                    if (answer === data.answers[i + data.leseverstehen_teil1.texts.length]) {
                        score++;
                        questionDiv.classList.add('correct');
                    } else {
                        questionDiv.classList.add('incorrect');
                    }
                }

                // Leseverstehen Teil 3
                for (let i = 0; i < data.leseverstehen_teil3.situations.length; i++) {
                    const selected = document.querySelector(`select[name="teil3_${i}"]`).value;
                    const answer = selected || '';
                    userAnswers.push(answer);
                    const questionDiv = teil3Div.children[i];
                    if (answer === data.answers[i + data.leseverstehen_teil1.texts.length + data.leseverstehen_teil2.questions.length]) {
                        score++;
                        questionDiv.classList.add('correct');
                    } else {
                        questionDiv.classList.add('incorrect');
                    }
                }

                // Sprachbausteine Teil 1
                for (let i = 0; i < data.sprachbausteine_teil1.options.length; i++) {
                    const selected = document.querySelector(`select[name="sprach1_${i + 21}"]`).value;
                    userAnswers.push(selected);
                    const questionDiv = sprach1QuestionsDiv.children[i];
                    if (selected === data.answers[i + (data.leseverstehen_teil1.texts.length + data.leseverstehen_teil2.questions.length + data.leseverstehen_teil3.situations.length)]) {
                        score++;
                        questionDiv.classList.add('correct');
                        document.getElementById(`sprach1_${i + 21}`).textContent = data.sprachbausteine_teil1.options[i][data.answers[i + (data.leseverstehen_teil1.texts.length + data.leseverstehen_teil2.questions.length + data.leseverstehen_teil3.situations.length)].charCodeAt(0) - 97];
                    } else {
                        questionDiv.classList.add('incorrect');
                        document.getElementById(`sprach1_${i + 21}`).textContent = selected ? data.sprachbausteine_teil1.options[i][selected.charCodeAt(0) - 97] : '';
                    }
                }

                // Sprachbausteine Teil 2
                for (let i = 0; i < 10; i++) {
                    const selected = document.querySelector(`select[name="sprach2_${i + 31}"]`).value;
                    const questionDiv = sprach2QuestionsDiv.children[i];
                    if (selected === data.answers[i + (data.leseverstehen_teil1.texts.length + data.leseverstehen_teil2.questions.length + data.leseverstehen_teil3.situations.length + data.sprachbausteine_teil1.options.length)]) {
                        score++;
                        questionDiv.classList.add('correct');
                        document.getElementById(`sprach2_${i + 31}`).textContent = data.sprachbausteine_teil1.options[i][data.answers[i + (data.leseverstehen_teil1.texts.length + data.leseverstehen_teil2.questions.length + data.leseverstehen_teil3.situations.length + data.sprachbausteine_teil1.options.length)].charCodeAt(0) - 65];
                    } else {
                        questionDiv.classList.add('incorrect');
                        document.getElementById(`sprach2_${i + 31}`).textContent = selected ? data.sprachbausteine_teil2.options[selected.charCodeAt(0) - 65] : '';
                    }
                }

                // Hiển thị kết quả
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `Bạn đã đạt ${score}/${totalQuestions} câu.`;
            });
        })
        .catch(error => {
            console.error('Lỗi khi tải JSON:', error);
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<p class="text-red-500">Lỗi: Không thể tải file test.json. Vui lòng kiểm tra file và chạy server cục bộ.</p>`;
        });
});