///<reference path="../../../typings/tsd.d.ts" />
///<reference path="services/notifications.service.ts" />
///<reference path="controllers/radar_structures.controller.ts" />
///<reference path="controllers/add_structure.controller.ts" />
///<reference path="controllers/notifications.controller.ts" />
///<reference path="controllers/structure_scan_modal.controller.ts" />

module radar {
  'use strict';

  export interface IUser {
    id: number;
    user_id: string;
    main_character: string;
    corporation: string;
    alliance: string;
  }

  export interface IStructure extends restangular.IElement {
    id: string;
    system: string;
    planet: string;
    corporation: string;
    alliance: string;
    standing: number;
    status: string;
    scan?: IScan;
    added_by?: IUser;
    created_on: Date;
    updated_on: Date;
  }

  export interface IScan extends restangular.IElement {
    id: string;
    content: string;
    added_by: IUser;
    created_on: Date;
    updated_on: Date;
  }

  export interface IErrorResponse {
    error: string;
  }

  var RadarApp = angular.module('radar', ['restangular', 'ui.bootstrap'])
    .service('NotificationsService', NotificationsService)
    .controller('RadarStructuresController', RadarStructuresController)
    .controller('AddStructureController', AddStructureController)
    .controller('NotificationsController', NotificationsController)
    .controller('StructureScanModalController', StructureScanModalController)
    .config(function (RestangularProvider: restangular.IProvider) {
      RestangularProvider.setBaseUrl('<%= API_ROOT %>');
      RestangularProvider.addResponseInterceptor(function(data, operation, what, url, response, deferred) {
            var extractedData;
            if (operation === 'getList') {
              extractedData = data.objects;
            } else {
              extractedData = data;
            }
            return extractedData;
          });
    })
}
