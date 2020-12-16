window.addEventListener('DOMContentLoaded',() => {
    socket.on('notification_alert', function(data, callback) {

        callback("success", data.id)
        addAlert("You have a new message")
        addMessage(data)
    })
    function addAlert(message){
        const alertContainer = document.querySelector('#notification-alert-container')
        const div = document.createElement('div')
        div.appendChild(document.createTextNode(message))
        div.className='alert alert-info'
        div.style.cssText=`
        position: sticky;
        top: 10px;
        `
        alertContainer.insertBefore(div, alertContainer.children[0])
    }
    function addMessage(msg){
        let container = document.getElementById('notifications-container')
        const table = createTable(msg)
        container.insertBefore(table, container.children[0])
    }
    function createTable({content, sender, timestamp}){
        const table = document.createElement('table')
        table.className = 'notification-table table table-hover'
        let message
        message = `<tr>
                    <td>
                        <span style="font-size:13px; font-weight: 700;">From @${sender.username}</span><br>
                        ${content}
                    </td>
                    <td class="text-right"style="font-size:13px;font-weight: 700; transform: translateY(15px)">${moment(new Date(timestamp)).fromNow()}</td>
                </tr>`
        table.innerHTML=message
        return table
    }
})