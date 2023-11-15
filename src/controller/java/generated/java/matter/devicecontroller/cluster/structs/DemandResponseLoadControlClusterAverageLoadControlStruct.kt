/*
 *
 *    Copyright (c) 2023 Project CHIP Authors
 *
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License.
 */
package matter.devicecontroller.cluster.structs

import matter.devicecontroller.cluster.*
import matter.tlv.ContextSpecificTag
import matter.tlv.Tag
import matter.tlv.TlvReader
import matter.tlv.TlvWriter

class DemandResponseLoadControlClusterAverageLoadControlStruct(val loadAdjustment: Byte) {
  override fun toString(): String = buildString {
    append("DemandResponseLoadControlClusterAverageLoadControlStruct {\n")
    append("\tloadAdjustment : $loadAdjustment\n")
    append("}\n")
  }

  fun toTlv(tlvTag: Tag, tlvWriter: TlvWriter) {
    tlvWriter.apply {
      startStructure(tlvTag)
      put(ContextSpecificTag(TAG_LOAD_ADJUSTMENT), loadAdjustment)
      endStructure()
    }
  }

  companion object {
    private const val TAG_LOAD_ADJUSTMENT = 0

    fun fromTlv(
      tlvTag: Tag,
      tlvReader: TlvReader
    ): DemandResponseLoadControlClusterAverageLoadControlStruct {
      tlvReader.enterStructure(tlvTag)
      val loadAdjustment = tlvReader.getByte(ContextSpecificTag(TAG_LOAD_ADJUSTMENT))

      tlvReader.exitContainer()

      return DemandResponseLoadControlClusterAverageLoadControlStruct(loadAdjustment)
    }
  }
}
