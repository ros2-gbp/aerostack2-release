// Copyright 2024 Universidad Politécnica de Madrid
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//    * Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//    * Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
//
//    * Neither the name of the Universidad Politécnica de Madrid nor the names of its
//      contributors may be used to endorse or promote products derived from
//      this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

/**
 * @file set_origin_service.hpp
 *
 * Set Origin service implementation as behavior tree node
 *
 * @authors Pedro Arias Pérez
 *          Rafael Perez-Segui
 *          Miguel Fernández Cortizas
 */

#include "as2_behavior_tree/action/set_origin.hpp"

namespace as2_behavior_tree
{
SetOrigin::SetOrigin(
  const std::string & xml_tag_name,
  const BT::NodeConfiguration & conf)
: nav2_behavior_tree::BtServiceNode<as2_msgs::srv::SetOrigin>(xml_tag_name,
    conf) {}

void SetOrigin::on_tick()
{
  getInput("latitude", this->request_->origin.latitude);
  getInput("longitude", this->request_->origin.longitude);
  getInput("altitude", this->request_->origin.altitude);
}

BT::NodeStatus SetOrigin::on_completion()
{
  return this->future_result_.get()->success ? BT::NodeStatus::SUCCESS :
         BT::NodeStatus::FAILURE;
}
}  // namespace as2_behavior_tree
