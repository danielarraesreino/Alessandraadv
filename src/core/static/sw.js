self.addEventListener('push', function (event) {
    const data = event.data ? event.data.json() : {};
    const title = data.title || 'Nova Atualização Jurídica';
    const options = {
        body: data.body || 'Um novo andamento foi detectado em seu processo.',
        icon: '/static/images/logo.png', // Adjust path as needed
        badge: '/static/images/icon.png'
    };
    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow('https://alessandradonadon.com/portal') // Adjust URL
    );
});
