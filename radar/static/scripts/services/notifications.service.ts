module radar {
    'use strict';

    export class Notification {
        type: string;
        message: string;

        constructor (type, message) {
            this.type = type;
            this.message = message;
        }
    }

    export class NotificationsService {

        $timeout: ng.ITimeoutService;
        notifications: Array<Notification> = [];

        /* @ngInject */
        constructor ($timeout: ng.ITimeoutService) {
            this.$timeout = $timeout;
        }

        addNotification (notification: Notification) {
            this.notifications.push(notification)
            var last = this.notifications.length - 1;
            this.$timeout(() => {
                this.notifications.splice(last, 1);
            }, 3500);
        }

        getNotifications () {
            return this.notifications;
        }

    }
}
