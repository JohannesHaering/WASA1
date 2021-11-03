from domain.loggingdata.LoggingData import LoggingData


class FilterGroups:
    """
    The information about the ports like the destination port
    """
    PORT_INFORMATION = ["destinationPort"]
    """
    A protocol uses flags to record answers
    PSH Flag: Push flag, the flag is set when the connection is set up, the data has to be process with the Data Stream Push Service
    URG Flag: Urgent flag, the data has to be processed with the signalling service 
    FIN Flag: Final Flag, the sender terminated the connection
    SYN Flag: Synchronisation Flag, information from the sender that he wants a connection
    RST Flag: Reset Flag, indicates that the sender wants to terminate the connection
    ACK Flag: Acknowledge Flag, acknowleges that the host received a data packet
    CWE Flag:
    ECE Flag: 
    """
    FLAGS = ["fwdPSHFlags", "bwdPSHFlags", "fwdURGFlags", "bwdURGFlags", "FINFlagCount", "SYNFlagCount", "RSTFlagCount",
             "PSHFlagCount", "ACKFlagCount", "URGFlagCount", "CWEFlagCount", "ECEFlagCount"]

    """
    Active means that an active connection is established    
    """
    GENERAL = ["activeMean", "activeStd", "activeMax", "activeMin", "idleMean", "idleStd", "idleMax", "idleMin"]

    """
    A protocol consists of multiple sent packets, also packets could be resent due to a timeout
    """
    PACKET_GENERAL = ["minPacketLength", "maxPacketLength", "packetLengthMean", "packetLengthStd",
                      "packetLengthVariance", "downUpRatio", "averagePacketSize"]

    """
    Sender to host -> Forward (fwd)
    Host to sender -> Backward (bwd)
    Bulk Data Throuhhput is an operation mode of TCP
    """
    PACKET_RATE = ["fwdPackets/s", "bwdPackets/s", "fwdAvgBytes/Bulk", "fwdAvgPackets/Bulk", "fwdAvgBulkRate",
                   "bwdAvgBytes/Bulk", "bwdAvgPackets/Bulk", "bwdAvgBulkRate"]

    """
    Information of forward packets
    """
    PACKET_GENERAL_INFORMATION_FWD = ["totalFwdPackets", "totalLengthFwdPackets", "fwdPacketLengthMax",
                                      "fwdPacketLengthMin", "fwdPacketLengthMean", "fwdPacketLengthStd",
                                      "fwdHeaderLength", "act_data_pkt_fwd"]

    """
    Information of backward packets
    """
    PACKET_GENERAL_INFORMATION_BWD = ["totalBackwardPackets", "totalLengthBwdPackets", "bwdPacketLengthMax",
                                      "bwdPacketLengthMin", "bwdPacketLengthMean", "bwdPacketLengthStd",
                                      "bwdHeaderLength"]

    """
    A Flow describes the sequence of multiple packets
    """
    FLOW = ["flowDuration", "flowBytes/s", "flowPackets/s", "flowIATMean", "flowIATStd", "flowIATMax", "flowIATMin",
            "subflowFwdPackets", "subflowBwdPackets"]

    """
    Packet information of forward packets
    """
    PACKET_SIZE_FWD = ["avgFwdSegmentSize", "min_seg_size_forward", "init_Win_bytes_forward", "subflowFwdBytes"]

    """
    Packet information of backward packets
    """
    PACKET_SIZE_BWD = ["avgBwdSegmentSize", "init_Win_bytes_backward", "subflowBwdBytes"]

    """
    IAT: Inter Arrival Time
    IAT information of forward messages
    """
    IAT_FWD = ["fwdIATTotal", "fwdIATMean", "fwdIATStd", "fwdIATMax", "fwdIATMin"]

    """
    IAT information of backward messages
    """
    IAT_BWD = ["bwdIATTotal", "bwdIATMean", "bwdIATStd", "bwdIATMax", "bwdIATMin"]


class Filter:
    @staticmethod
    def getAvailableFilters() -> list:
        return ["all_features", "general_information", "forward_information", "backward_information"]

    @staticmethod
    def filter(filterName: str, features: LoggingData) -> list:
        if filterName == "general_information": return Filter.__filterGeneralInformation(features)
        if filterName == "forward_information": return Filter.__filterForwardInformation(features)
        if filterName == "backward_information": return Filter.__filterBackwardInformation(features)

        return Filter.__allFilter(features)

    @staticmethod
    def __allFilter(loggingData: LoggingData) -> list:
        return list(loggingData.features.values())

    @staticmethod
    def __filterForwardInformation(loggingData: LoggingData) -> list:
        wanted = FilterGroups.FLAGS + FilterGroups.PACKET_GENERAL + FilterGroups.PACKET_GENERAL_INFORMATION_FWD \
                 + FilterGroups.PACKET_SIZE_FWD + FilterGroups.IAT_FWD

        return Filter.__applyFilter(loggingData.features, wanted)

    @staticmethod
    def __filterBackwardInformation(loggingData: LoggingData) -> list:
        wanted = FilterGroups.FLAGS + FilterGroups.PACKET_GENERAL + FilterGroups.PACKET_GENERAL_INFORMATION_BWD \
                 + FilterGroups.PACKET_SIZE_BWD + FilterGroups.IAT_BWD

        return Filter.__applyFilter(loggingData.features, wanted)

    @staticmethod
    def __filterGeneralInformation(loggingData: LoggingData) -> list:
        wanted = FilterGroups.FLAGS + FilterGroups.GENERAL + FilterGroups.PACKET_GENERAL \
                 + FilterGroups.PACKET_GENERAL_INFORMATION_FWD + FilterGroups.PACKET_GENERAL_INFORMATION_BWD

        return Filter.__applyFilter(loggingData.features, wanted)

    @staticmethod
    def __applyFilter(toFilter: dict, keys: list) -> list:
        filtered: list = []
        for key in keys: filtered += [toFilter[key]]
        return list(filtered)
