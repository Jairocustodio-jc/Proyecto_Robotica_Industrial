
"use strict";

let GetJointPosition = require('./GetJointPosition.js')
let SetActuatorState = require('./SetActuatorState.js')
let SetDrawingTrajectory = require('./SetDrawingTrajectory.js')
let SetJointPosition = require('./SetJointPosition.js')
let GetKinematicsPose = require('./GetKinematicsPose.js')
let SetKinematicsPose = require('./SetKinematicsPose.js')

module.exports = {
  GetJointPosition: GetJointPosition,
  SetActuatorState: SetActuatorState,
  SetDrawingTrajectory: SetDrawingTrajectory,
  SetJointPosition: SetJointPosition,
  GetKinematicsPose: GetKinematicsPose,
  SetKinematicsPose: SetKinematicsPose,
};
