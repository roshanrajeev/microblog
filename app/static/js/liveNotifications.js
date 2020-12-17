window.addEventListener('DOMContentLoaded', () => {
    socket.on('new messages', function(msg) {
        handleNotification(msg)
    })
    
    function handleNotification(msg){
        const item = document.querySelector('#nav-item-notification')
        if(!item.children[0].classList.contains('nav-item-notification-icon')){
            const span = document.createElement('span')
            span.className='nav-item-notification-icon'
            span.style.cssText=`
                background-color: orange; 
                position:absolute;top: 50%;
                transform: translate(0, -51%);
                left: -8px; 
                width: 8px; 
                height: 8px; 
                border-radius: 50%;
            `
            item.insertBefore(span, item[0])
        }
    }
})