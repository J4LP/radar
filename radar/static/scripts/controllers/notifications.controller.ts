module radar {
    'use strict';

    interface INotificationsScope extends ng.IScope {
        notifications: Array<Notification>;
        events: NotificationsController;
        getCSSClass: Function;
    }

    export class NotificationsController {
        $scope: INotificationsScope;
        NotificationsService: NotificationsService;

        /* @ngInject */
        constructor($scope: INotificationsScope, NotificationsService: NotificationsService) {
            this.$scope = $scope;
            this.$scope.events = this;
            this.NotificationsService = NotificationsService;
            this.$scope.notifications = this.NotificationsService.getNotifications();
            this.$scope.getCSSClass = this.getCSSClass;
        }

        closeNotification (index: number) {
            this.$scope.notifications.splice(index, 1)
        }

        getCSSClass (notification: Notification) {
            if (notification.type == 'success') {
                return 'alert-success';
            } else if (notification.type == 'warning') {
                return 'alert-warning';
            } else if (notification.type == 'danger') {
                return 'alert-danger';
            } else {
                return 'alert-info'
            }
        }
    }
}
