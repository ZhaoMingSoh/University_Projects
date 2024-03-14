class message:
    def __init__(self, message_type, source_id, proposal_id, proposal_val, accepted_proposal_id, accepted_proposal_val, bool_accepted_proposal) -> None:
        self.message_type = message_type
        self.source_id = source_id
        self.proposal_id = proposal_id
        self.proposal_val = proposal_val
        self.accepted_proposal_id = accepted_proposal_id
        self.accepted_proposal_val = accepted_proposal_val
        self.bool_accepted_proposal = bool_accepted_proposal