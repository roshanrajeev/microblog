let currentPage = 1;
window.addEventListener('DOMContentLoaded', () => {
    handlePageLoad()
    const btn = document.querySelector('#load-messages')
    btn.addEventListener('click', (e)=>{
        currentPage++;
        handlePageLoad()
    })
})
async function handlePageLoad(){
    let container = document.getElementById('notifications-container')
    let newNotifications = await getNewNotifications(currentPage)
    let messages = newNotifications.messages
    if(!newNotifications.hasNext){
        const btn = document.querySelector('#load-messages')
        btn.disabled=true
    }
    messages.forEach(n => {
        const table = createTable(n)
        container.appendChild(table)
    })
}
async function getNewNotifications(page){
    const response = await fetch(`/load-notifications?page=${page}`, {
        method: 'GET',
        headers:{
            'Content-Type': 'application/json'
        }
    })
    const data = await response.json()
    return data
}
function createTable({content, id, timestamp}){
    const table = document.createElement('table')
    table.className = 'notification-table table table-hover'
    const msg = `<tr>
                    <td>
                        <span style="font-size:13px">From @caity</span><br>
                        ${content}
                    </td>
                    <td class="text-right"style="font-size:13px; transform: translateY(15px)">${moment(timestamp).fromNow()}</td>
                </tr>`
    table.innerHTML=msg
    return table
}