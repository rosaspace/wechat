
  // self.addEventListener('install', function (event) {
  //   event.waitUntil(
  //     caches.open('my-cache').then(function (cache) {
  //       return cache.addAll(['/offline/', '/static/icons/favicon.ico']);
  //     })
  //   );
  // });

  // self.addEventListener('fetch', function (event) {
  //   var requestUrl = new URL(event.request.url);
  //   if (requestUrl.origin === location.origin) {
  //     if ((requestUrl.pathname === '/')) {
  //       event.respondWith(caches.match('/offline/'));
  //       return;
  //     }
  //   }
  //   event.respondWith(
  //     caches.match(event.request).then(function (response) {
  //       return response || fetch(event.request);
  //     })
  //   );
  // });

self.addEventListener('install', function(event) {
    console.log('Service Worker installing...');
});

self.addEventListener('activate', function(event) {
    console.log('Service Worker activating...');
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});