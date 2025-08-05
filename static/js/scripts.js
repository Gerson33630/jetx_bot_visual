document.addEventListener('DOMContentLoaded', function() {
    // Atualização automática a cada 15 segundos
    setInterval(updateData, 15000);
    
    // Função para buscar novos dados
    function updateData() {
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                updateUI(data);
            })
            .catch(error => {
                console.error('Erro ao atualizar dados:', error);
            });
    }
    
    // Função para atualizar a interface
    function updateUI(data) {
        // Atualizar o multiplicador atual
        if (data.current) {
            document.querySelector('.multiplier-display').className = `multiplier-display ${data.current.css_class}`;
            document.querySelector('.multiplier-display .value').textContent = data.current.value;
            document.querySelector('.category').textContent = data.current.category;
            document.querySelector('.category').className = `category ${data.current.css_class}`;
            document.querySelector('.protection').textContent = `Proteção recomendada: ${data.current.protection}x`;
            document.querySelector('.time').textContent = new Date(data.current.time).toLocaleTimeString();
        }
        
        // Atualizar estatísticas
        document.querySelector('.stat-value.green').textContent = data.streak;
        document.querySelectorAll('.stat-value')[1].textContent = data.trends ? data.trends.green_probability.toFixed(2) : 'N/A';
        document.querySelectorAll('.stat-value')[2].textContent = data.trends ? data.trends.volatility.toFixed(2) : 'N/A';
        
        // Atualizar aviso
        const warningElement = document.querySelector('.alert.warning');
        if (data.warning) {
            if (!warningElement) {
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert warning';
                alertDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i><span>${data.warning}</span>`;
                document.querySelector('.app-main').insertBefore(alertDiv, document.querySelector('.history-section'));
            } else {
                warningElement.querySelector('span').textContent = data.warning;
            }
        } else if (warningElement) {
            warningElement.remove();
        }
        
        // Atualizar último verde
        if (data.last_green) {
            document.querySelectorAll('.stat-value')[3].textContent = data.last_green.value;
            document.querySelector('.stat-sublabel').textContent = new Date(data.last_green.time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
        
        // Atualizar histórico (simplificado - em produção seria mais complexo)
        // Nota: Em uma aplicação real, seria melhor usar um framework como React/Vue para isso
        
        // Atualizar timestamp
        document.querySelector('.last-update').textContent = `Última atualização: ${data.last_update}`;
    }
    
    // Notificações (se permitido pelo usuário)
    if ('Notification' in window) {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                console.log('Permissão para notificações concedida');
            }
        });
    }
});
