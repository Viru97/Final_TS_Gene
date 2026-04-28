/*
 * Copyright (C) 2016 Open Source Robotics Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
*/

#include <rclcpp/rclcpp.hpp>

// Gazebo Harmonic Headers
#include <gz/sim/System.hh>
#include <gz/sim/Model.hh>
#include <gz/sim/components/Pose.hh>
#include <gz/sim/components/Actor.hh>
#include <gz/plugin/Register.hh>

namespace obstacles
{
  // In Gazebo Harmonic, plugins are Systems that inherit from specific interfaces
  class StickPlugin :
    public gz::sim::System,
    public gz::sim::ISystemConfigure,
    public gz::sim::ISystemPostUpdate
  {
  public:
    StickPlugin() = default;
    ~StickPlugin() override = default;

    // This replaces the old Load() method
    void Configure(const gz::sim::Entity &_entity,
                   const std::shared_ptr<const sdf::Element> &_sdf,
                   gz::sim::EntityComponentManager &_ecm,
                   gz::sim::EventManager &_eventMgr) override
    {
      // 1. Initialize ROS 2 if it hasn't been initialized yet
      if (!rclcpp::ok()) {
        rclcpp::init(0, nullptr);
      }

      // 2. Create the ROS 2 Node
      ros_node_ = rclcpp::Node::make_shared("stick_plugin_node");

      // 3. Store the model entity so we can query it later
      model_ = gz::sim::Model(_entity);

      RCLCPP_INFO(ros_node_->get_logger(), "StickPlugin successfully loaded in Gazebo Harmonic!");
    }

    // This replaces the old OnUpdate() method
    void PostUpdate(const gz::sim::UpdateInfo &_info,
                    const gz::sim::EntityComponentManager &_ecm) override
    {
      // We only want to process updates if the simulation is not paused
      if (_info.paused) return;

      // 4. In ECS, we query the Entity Component Manager (ECM) for the Pose component of our model
      auto poseComp = _ecm.Component<gz::sim::components::Pose>(model_.Entity());

      if (poseComp) {
        auto pose = poseComp->Data();
        RCLCPP_INFO_STREAM(ros_node_->get_logger(),
          "Actor world Pose: " << pose.Pos().X() << ", "
                               << pose.Pos().Y() << ", "
                               << pose.Pos().Z());
      }
    }

  private:
    rclcpp::Node::SharedPtr ros_node_;
    gz::sim::Model model_;
  };
}

// 5. Register the plugin with Gazebo Harmonic (Replaces GZ_REGISTER_MODEL_PLUGIN)
GZ_ADD_PLUGIN(obstacles::StickPlugin,
              gz::sim::System,
              obstacles::StickPlugin::ISystemConfigure,
              obstacles::StickPlugin::ISystemPostUpdate)

GZ_ADD_PLUGIN_ALIAS(obstacles::StickPlugin, "obstacles::StickPlugin")