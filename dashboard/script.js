document.addEventListener('DOMContentLoaded', function() {
    let stompClient;

    const stompConfig = {
        connectHeaders: {
            login: "dashboard_user",
            passcode: "dashboard_pass"
        },
        brokerURL: 'ws://localhost:15674/ws',
        reconnectDelay: 200,
        onConnect: function (frame) {
            console.log("Connected to RabbitMQ STOMP");
            stompClient.subscribe('/queue/control.relays.status', function (message) {
                updateStatus(JSON.parse(message.body));
                message.ack();
            }, { ack: 'client'});
        }
        
    };

    stompClient = new StompJs.Client(stompConfig);
    stompClient.activate();

    function sendCommand(board, relay, action) {
        const message = JSON.stringify({ [relay]: action });
        const routingKey = `control.relays.cmd.${board}`;
        console.log(`Sending message: ${message} to routingKey: ${routingKey}`);
        stompClient.publish({destination: `/topic/${routingKey}`, body: message});
    }

    function updateStatus(data) {
        Object.keys(data.relays).forEach(relay => {
            const statusElement = document.getElementById(`status-${relay.toLowerCase()}`);
            if (statusElement) {
                statusElement.className = `status-indicator ${data.relays[relay]}`;
            }
        });
        if (data.temp !== undefined) {
            const tempElement = document.getElementById('temp-value');
            if (tempElement) {
                tempElement.textContent = data.temp.toFixed(2);
            }
        }
    }

    document.querySelectorAll('.relay-control').forEach(button => {
        button.addEventListener('click', function() {
            const board = this.getAttribute('data-board');
            const relay = this.getAttribute('data-relay');
            const action = this.getAttribute('data-action');
            sendCommand(board, relay, action);
        });
    });
});
