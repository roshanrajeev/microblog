window.addEventListener('DOMContentLoaded', () => {
    socket.on('new messages', function(msg) {
        handleNotification(msg)
    })
    
    function handleNotification(msg){
        const itemSM = document.querySelector('.nav-item-notification-sm')
        const itemLG = document.querySelector('.nav-item-notification-lg')
        if(!itemSM.children[0].classList.contains('nav-item-notification-icon')){
            const span = document.createElement('span')
            span.className='nav-item-notification-icon'
            span.style.cssText=`
            background-color: orange; 
            position:absolute;top: 50%;
            transform: translate(21px, -115%);
            left: -8px; 
            width: 8px; 
            height: 8px; 
            border-radius: 50%;
            `
            itemSM.insertBefore(span, itemSM[0])
        }
        if(!itemLG.children[0].classList.contains('nav-item-notification-icon')){
            const span = document.createElement('span')
            span.className='nav-item-notification-icon'
            span.style.cssText=`
            background-color: orange; 
            position:absolute;top: 50%;
            transform: translate(14px, -115%);
            left: -8px; 
            width: 8px; 
            height: 8px; 
            border-radius: 50%;
            `
            itemLG.insertBefore(span, itemLG[0])
        }
    }
})