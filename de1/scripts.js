document.addEventListener('DOMContentLoaded', () => {
    // Tùy chọn tĩnh cho Leseverstehen Teil 3
    const options = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'X'];

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
                    <p class="content"><span class="question-number">${index + 1}.</span> ${text.replace(/\r\n/g, '<br>')}</p>
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
            teil3Image.src = `/de/images/${data.leseverstehen_teil3.image_path.replace(/\\/g, '/').replace(/^\/+/, '').replace(/^images\//, '')}`;
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
                        document.getElementById(`sprach2_${i + 31}`).textContent = data.sprachbausteine_teil2.options[data.answers[i + (data.leseverstehen_teil1.texts.length + data.leseverstehen_teil2.questions.length + data.leseverstehen_teil3.situations.length + data.sprachbausteine_teil1.options.length)].charCodeAt(0) - 65];
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