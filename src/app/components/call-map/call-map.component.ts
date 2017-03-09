import { Component, OnInit, ViewContainerRef, ViewRef, ViewChild, ElementRef } from '@angular/core';

import { SocketConnectionService, CoordinatesConverterService } from '../../shared';
import { WsCallNotification, CallNoteDescription } from '../../core';

@Component({
  selector: 'jlm-call-map',
  templateUrl: './call-map.component.html',
  styleUrls: ['./call-map.component.scss']
})
export class CallMapComponent implements OnInit {
  @ViewChild('svgDocument') svgRef: ElementRef;
  notifications: WsCallNotification[] = [];

  constructor(
    private scs: SocketConnectionService,
    private coordsCvrtr: CoordinatesConverterService) {}

  ngOnInit() {
    this.scs.room.addEventListener('message', (event) => this.onCallNotification(event), false);
  }

  getSvgDimensions(): {width: number, height: number} {
    const natel = this.svgRef;
    return {width: 1366, height: 768};
  }

  onCallNotification(event: MessageEvent) {
    const rawNotification = JSON.parse(event.data) as CallNoteDescription;
    const call: WsCallNotification = {
      caller: {
        gps: {
            lat: +rawNotification.call.caller.lat,
            lng: +rawNotification.call.caller.lng
        }
      },
      callee: {
          gps: {
            lat: +rawNotification.call.target.lat,
            lng: +rawNotification.call.target.lng
          }
      }
    };
    const callerSvgCoords = this.coordsCvrtr.getSvgLocation(call.caller.gps.lat, call.caller.gps.lng);
    const calleeSvgCoords = this.coordsCvrtr.getSvgLocation(call.callee.gps.lat, call.callee.gps.lng);
    const {width: mapWidth, height: mapHeight} = this.getSvgDimensions();
    call.caller.svg = {x: callerSvgCoords.x * mapWidth, y: callerSvgCoords.y * mapHeight};
    call.callee.svg = {x: calleeSvgCoords.x * mapWidth, y: calleeSvgCoords.y * mapHeight};
    this.notifications.push(call);
  }

}
