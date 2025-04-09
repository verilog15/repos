// Released under the MIT License. See LICENSE for details.

#ifndef BALLISTICA_BASE_ASSETS_ASSETS_SERVER_H_
#define BALLISTICA_BASE_ASSETS_ASSETS_SERVER_H_

#include <cstdio>
#include <list>
#include <vector>

#include "ballistica/base/base.h"
#include "ballistica/shared/foundation/object.h"

namespace ballistica::base {

class AssetsServer {
 public:
  AssetsServer();
  void OnMainThreadStartApp();
  void PushBeginWriteReplayCall(uint16_t protocol_version);
  void PushEndWriteReplayCall();
  void PushAddMessageToReplayCall(const std::vector<uint8_t>& data);
  void PushPendingPreload(Object::Ref<Asset>* asset_ref_ptr);
  auto event_loop() const -> EventLoop* { return event_loop_; }

 private:
  void OnAppStartInThread_();
  void Process_();
  void WriteReplayMessages_();

  std::list<std::vector<uint8_t> > replay_messages_;
  std::vector<Object::Ref<Asset>*> pending_preloads_;
  std::vector<Object::Ref<Asset>*> pending_preloads_audio_;
  EventLoop* event_loop_{};
  FILE* replay_out_file_{};
  Timer* process_timer_{};
  size_t replay_bytes_written_{};
  size_t replay_message_bytes_{};
  bool writing_replay_{};
  bool replays_broken_{};
};

}  // namespace ballistica::base

#endif  // BALLISTICA_BASE_ASSETS_ASSETS_SERVER_H_
